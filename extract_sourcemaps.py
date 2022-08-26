#!/usr/bin/env python
"""Extract source maps from a given URL."""
# Описание формата: https://www.bugsnag.com/blog/source-maps
import argparse
import ast
import functools
import pathlib
import queue
import re
import sys
import threading
from enum import Enum, auto
from typing import Sequence, TypedDict
from urllib.parse import urljoin, urlsplit

import bs4
import requests

FILENAME_RE = re.compile(r'/(?:chunk\w+|app)\.[0-9a-f]{8,}\.js$')

# React
# ...
# export default __webpack_public_path__ + '...'
# ...
# Vue
# module.exports = __webpack_public_path__ + "...";

WEBPACK_PUBLIC_PATH_RE = re.compile(
    r'__webpack_public_path__ \+ (\'(?:\\\'|[^\'])*\'|"(?:\\"|[^"])*")'
)

requests.packages.urllib3.disable_warnings()
stderr = functools.partial(print, file=sys.stderr)


CSI = '\033['


class Color(Enum):
    black = 30
    red = auto()
    green = auto()
    yellow = auto()
    blue = auto()
    magenta = auto()
    cyan = auto()
    white = auto()

    def wrap(self, s: str) -> str:
        return f'{CSI}{self.value}m{s}{CSI}0m'

    __call__ = wrap


def enquote(s: str) -> str:
    return ast.literal_eval(s)


class SourceMapDict(TypedDict):
    # Declares which version of the source map spec is being used, like a <!DOCTYPE> in html.
    version: int
    # A list of input source files that were used to generate the output.
    sources: list[str]
    # A list of identifiers used in the source code which were changed in or removed from the output.
    names: list[str]
    # This is the clever bit! These comma and semi-colon separated values are base64-encoded VLQ
    # values that point from every position in the output back to positions in the input sources.
    mappings: str
    # This optional field can include the original source content for each file in
    # the "sources" property. This option should only be omitted if the tool using
    # the source map can retrieve the sources via url or from the filesystem.
    sourcesContent: list[str]
    # A prefix to add to each entry in the "sources" property when looking them up
    # on the network/disk.
    sourceRoot: str
    # The name of the file this source map is for.
    file: str


def get_client() -> requests.Session:
    client = requests.session()
    client.headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36',
            'Referer': 'https://www.google.com',
        }
    )
    return client


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('url', help='target url')
    parser.add_argument(
        '-o',
        '--output-dir',
        '--output',
        help='output directory',
        default='output',
    )
    parser.add_argument(
        '-w',
        '--workers',
        help='number of worker threads',
        default=10,
    )
    args = parser.parse_args(argv)
    target_url = args.url
    output_dir = (
        pathlib.Path(args.output_dir).resolve() / urlsplit(target_url).netloc
    )

    client = get_client()

    try:
        r = client.get(target_url, verify=False)
        s = bs4.BeautifulSoup(r.text, 'lxml')
        if scripts := s.find_all('script', src=FILENAME_RE):
            q = queue.Queue()
            for scr in scripts:
                u = urljoin(r.url, scr['src'] + '.map')
                q.put_nowait(u)
            threads = []
            for _ in range(min(q.qsize(), args.workers)):
                t = threading.Thread(
                    target=extract_sourcemaps, args=(q, output_dir)
                )
                t.start()
                threads.append(t)
            q.join()
            for t in threads:
                t.join()
            stderr(Color.yellow('All tasks completed!'))
        else:
            stderr(Color.red('nothing is found :-('))
    except Exception as e:
        stderr(Color.red(f'unexpected error: {e}'))


def normalize_source_name(s: str) -> str:
    assert s.startswith('webpack://')
    return s[len('webpack://') :].lstrip('/')


def save_sources(
    source_map: SourceMapDict,
    output_dir: pathlib.Path,
    sourcemap_url: str,
    client: requests.Session,
) -> None:
    for source, contents in zip(
        map(lambda v: source_map['sourceRoot'] + v, source_map['sources']),
        source_map['sourcesContent'],
    ):
        source = normalize_source_name(source)
        stderr(Color.blue(f'{source=}'))
        source_path = (output_dir / source).resolve()
        # Проверка на выход за пределы каталога
        if not source_path.is_relative_to(output_dir):
            stderr(Color.red(f'ouf of directory: {source_path}'))
            continue
        if source_path.exists():
            stderr(Color.red(f'already exists: {source_path}'))
            continue
        source_path.parent.mkdir(parents=True, exist_ok=True)
        if match := WEBPACK_PUBLIC_PATH_RE.search(contents):
            asset_path = enquote(match.group(1))
            asset_url = urljoin(sourcemap_url, '/' + asset_path)
            r = client.get(asset_url, verify=False)
            if r.status_code == 200:
                source_path.write_bytes(r.content)
                stderr(Color.green(f'asset saved: {source_path}'))
            else:
                stderr(Color.red(f'asset not found: {asset_url}'))
        else:
            source_path.write_text(contents)
            stderr(Color.green(f'saved: {source_path}'))


def extract_sourcemaps(q: queue.Queue, output_dir: pathlib.Path) -> None:
    client = get_client()
    while not q.empty():
        try:
            sourcemap_url = q.get()
            r = client.get(sourcemap_url, verify=False)
            if not (r.status_code == 200 and 'webpack://' in r.text):
                stderr(Color.red(f'source map not found: {sourcemap_url}'))
                continue
            try:
                data = r.json()
            except requests.exceptions.JSONDecodeError:
                stderr(Color.red(f'invalid source map: {sourcemap_url}'))
                continue
            save_sources(data, output_dir, sourcemap_url, client)
        except Exception as e:
            stderr(Color.red(f'error: {e}'))
        finally:
            q.task_done()


if __name__ == '__main__':
    sys.exit(main())
