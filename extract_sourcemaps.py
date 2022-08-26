#!/usr/bin/env python
"""Extract source maps from a given URL."""
# TODO: разобраться почему среди соурсов многократно встречаются одинаковые файлы
# типа webpack://./src/App.vue, webpack:///src/App.vue и webpack://./src/App.vue?abcd
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
    version: int
    sources: list[str]
    sourcesContent: list[str]
    ...
    sourceRoot: str


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
        else:
            stderr(Color.red('nothing is found :-('))
    except Exception as e:
        stderr(Color.red(f'unexpected error: {e}'))


def normalize_source_path(path: str) -> str:
    assert path.startswith('webpack://')
    path = path[len('webpack://') :]
    return path.lstrip('/')


def save_sources(
    source_map: SourceMapDict,
    output_dir: pathlib.Path,
    sourcemap_url: str,
    client: requests.Session,
) -> None:
    for path, contents in zip(
        source_map['sources'], source_map['sourcesContent']
    ):
        path = normalize_source_path(path)
        file_path = (output_dir / path).resolve()
        # Проверка на выход за пределы каталога
        if not file_path.is_relative_to(output_dir):
            stderr(Color.red(f'ouf of directory: {file_path}'))
            continue
        if file_path.exists():
            stderr(Color.cyan(f'already exists: {file_path}'))
            continue
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if match := WEBPACK_PUBLIC_PATH_RE.search(contents):
            asset_path = enquote(match.group(1))
            asset_url = urljoin(sourcemap_url, '/' + asset_path)
            r = client.get(asset_url, verify=False)
            if r.status_code == 200:
                file_path.write_bytes(r.content)
                stderr(Color.green(f'asset saved: {file_path}'))
            else:
                stderr(Color.red(f'asset not found: {asset_url}'))
        else:
            file_path.write_text(contents)
            stderr(Color.green(f'saved: {file_path}'))


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
