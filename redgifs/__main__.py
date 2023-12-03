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

# TODO: Use rich for pretty console messages.

import re
import sys
import argparse
import platform
import importlib.metadata
from typing import Optional

import aiohttp
import requests
from yarl import URL

import redgifs
from redgifs.models import GIF

parser = argparse.ArgumentParser(prog='redgifs')
parser.add_argument('link', nargs='?', help='Enter a RedGifs URL', metavar='URL')
parser.add_argument('--folder', help='Folder to download the video(s) to.', metavar='FOLDER')
parser.add_argument('--list', help='Download GIFs from a txt file containing URLs seperated by a newline.', metavar='FILE')
parser.add_argument('--version', help='Show redgifs version info.', action='store_true')
parser.add_argument('--quality', help='The video quality of the GIF to download. Available options are: "sd" and "hd".', metavar='QUALITY', default="hd")
args = parser.parse_args()

session = requests.Session()
client = redgifs.API(session=session)

USERNAME_RE = re.compile(r'https:\/\/(www\.)?redgifs\.com\/users\/(?P<username>\w+)')

def show_version() -> None:
    entries = []

    entries.append('- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))
    version_info = redgifs.version_info
    entries.append('- redgifs v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info))
    if version_info.releaselevel != 'final':
        version = importlib.metadata.version('redgifs')
        if version:
            entries.append(f'    - redgifs metadata: v{version}')

    entries.append(f'- aiohttp v{aiohttp.__version__}')
    uname = platform.uname()
    entries.append('- system info: {0.system} {0.release} {0.version}'.format(uname))
    print('\n'.join(entries))

def get_quality(q: str, gif: GIF) -> str:
    if q.lower() not in ['sd', 'hd']:
        raise TypeError('Valid quality options are "sd" or "hd"')
    if q.lower() == 'sd':
        return gif.urls.sd
    if q.lower() == 'hd':
        return gif.urls.hd
    # Shouldn't reach here
    else:
        return gif.urls.hd

def start_dl(url: str, *, folder: Optional[str], quality: str) -> None:
    yarl_url = URL(url)
    if 'redgifs' not in str(yarl_url.host):
        raise TypeError(f'"{url}" is not a valid redgifs URL')

    # Handle 'normal' URLs, i.e, a direct link from browser (eg: "https://redgifs.com/watch/deeznuts")
    if 'watch' in yarl_url.path:
        id = yarl_url.path.split('/')[-1]
        gif = client.get_gif(id)
        gif = get_quality(quality, gif)
        filename = f'{gif.split("/")[3].split(".")[0]}.mp4'
        print(f'Downloading {id}...')
        if folder:
            client.download(gif, f'{folder}/{filename}')
        else:
            client.download(gif, f'{filename}')
        print('Download complete.\n')

    # Handle /users/ URLs (eg: https://redgifs.com/users/redgifs)
    if '/users/' in yarl_url.path:
        match = re.match(USERNAME_RE, str(yarl_url))
        if not match:
            raise TypeError(f'Not a valid /users/ URL: {yarl_url}')
        user = match.groupdict()['username']
        data = client.search_creator(user)
        curr_page = data.page
        total_pages = data.pages
        total_gifs = data.gifs
        total = data.total
        done = 0

        # Case where there is only 1 page
        if curr_page == total_pages:
            for gif in total_gifs:
                gif = get_quality(quality, gif)
                filename = f'{gif.split("/")[3].split(".")[0]}.mp4'
                try:
                    if folder:
                        client.download(gif, f'{folder}/{filename}')
                    else:
                        client.download(gif, f'{filename}')
                    done += 1
                    print(f'Downloaded {done}/{total} GIFs')
                except Exception as e:
                    if isinstance(e, FileNotFoundError):
                        print(f'[!] An error occured while downloading: {e}\nMake sure you have a folder called "{folder}" in the current directory.')
                        exit(1)
                    else:
                        print(f'[!] Error occurred when downloading {url}:\n{e}. Continuing...')
                        continue

            print(f'\nDownloaded {done}/{total} videos of "{user}" {f"to {folder} folder" if folder else ""} sucessfully')

        # If there's more than 1 page
        while curr_page != total_pages:
            for gif in total_gifs:
                gif = get_quality(quality, gif)
                filename = f'{gif.split("/")[3].split(".")[0]}.mp4'
                try:
                    if folder:
                        client.download(gif, f'{folder}/{filename}')
                    else:
                        client.download(gif, filename)
                    done += 1
                    print(f'Downloaded {done}/{total} GIFs')
                except Exception as e:
                    if isinstance(e, FileNotFoundError):
                        print(f'[!] An error occured while downloading: {e}\nMake sure you have a folder called "{folder}" in the current working directory.')
                        exit(1)
                    else:
                        print(f'[!] Error occurred when downloading {url}:\n{e}. Continuing...')
                        continue
            curr_page += 1
            total_gifs.clear()
            data = client.search_creator(user, page=curr_page)
            total_gifs.extend(data.gifs)

        print(f'\nDownloaded {done}/{total} videos of "{user}" {f"to {folder} folder" if folder else ""} sucessfully')

def main() -> None:
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.link:
        client.login()
        start_dl(args.link, folder=args.folder, quality=args.quality)
        exit(0)

    if args.list:
        client.login()
        with open(args.list) as f:
            for url in f.readlines():
                start_dl(url, folder=args.folder, quality=args.quality)
            exit(0)

    if args.version:
        show_version()

if __name__ == '__main__':
    main()
