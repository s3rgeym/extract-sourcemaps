#!/usr/bin/env python
"""Extract source maps from a given URL."""
import argparse
import functools
import pathlib
import queue
import re
import sys
import threading
from typing import TypedDict
from urllib.parse import urljoin, urlsplit

import bs4
import requests

FILENAME_RE = re.compile(r'/(?:chunk\w+|app)\.[0-9a-f]{8,}\.js$')

requests.packages.urllib3.disable_warnings()
stderr = functools.partial(print, file=sys.stderr)


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('url', help='target url')
    parser.add_argument(
        '-o',
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
    args = parser.parse_args()
    target_url = args.url
    output_dir = pathlib.Path(args.output) / urlsplit(target_url).netloc

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
            stderr('nothing is found :-(')
    except Exception as e:
        stderr('unexpected error:', e)


def normalize_source_path(path: str) -> str:
    assert path.startswith('webpack://')
    path = path[len('webpack://') :]
    return path.lstrip('./')


def save_sources(source_map: SourceMapDict, output_dir: pathlib.Path) -> None:
    for path, contents in zip(
        source_map['sources'], source_map['sourcesContent']
    ):
        path = normalize_source_path(path)
        file_path = output_dir / path
        if file_path.exists():
            stderr('already exists:', path)
            continue
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as f:
            f.write(contents)
        stderr('saved:', file_path)


def extract_sourcemaps(q: queue.Queue, output_dir: pathlib.Path) -> None:
    client = get_client()
    while not q.empty():
        try:
            u = q.get()
            r = client.get(u, verify=False)
            if not (r.status_code == 200 and 'webpack://' in r.text):
                stderr('source map not found:', u)
                continue
            try:
                data = r.json()
            except requests.exceptions.JSONDecodeError:
                stderr('invalid source map:', u)
                continue
            save_sources(data, output_dir)
        except Exception as e:
            stderr('error:', e)
        finally:
            q.task_done()


if __name__ == '__main__':
    main()
