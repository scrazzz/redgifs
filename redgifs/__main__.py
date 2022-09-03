"""
The MIT License (MIT)

Copyright (c) 2022-present scrazzz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import sys
import argparse

import requests
from yarl import URL

import redgifs

parser = argparse.ArgumentParser(prog = 'redgifs')
parser.add_argument('-dl', '--download', help = 'Download the GIF from given link', metavar = '')
parser.add_argument('-l', '--list', help = 'Download GIFs from a list of URLs', metavar = '')
args = parser.parse_args()

session = requests.Session()
client = redgifs.API(session=session)

def save_to_file(mp4_link):
    headers = client.http.headers
    r = session.get(mp4_link, headers = headers, stream = True)
    file_name = mp4_link.split('/')[-1]
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024 * 1024):
            if chunk:
                f.write(chunk)
    
    print(f'\nDownloaded: {file_name}')

def start_dl(url: str):
    yarl_url = URL(url)
    if 'redgifs' not in str(yarl_url.host):
        raise TypeError(f'"{url}" is an invalid redgifs URL')

    # Handle 'normal' URLs, i.e, a direct link from browser (eg: "https://redgifs.com/watch/deeznuts")
    if 'watch' in yarl_url.path:
        id = yarl_url.path.strip('/watch/')
        hd = client.get_gif(id).urls.hd
        print(f'Downloading {id}...')
        save_to_file(hd)

def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.download:
        start_dl(args.download)

    if args.list:
        with open(args.list) as f:
            for url in f.readlines():
                start_dl(url)

if __name__ == '__main__':
    main()