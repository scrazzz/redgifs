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

from __future__ import annotations

import click
import re
import yarl
from typing import Iterable, Optional, TYPE_CHECKING

import redgifs

if TYPE_CHECKING:
    from redgifs.models import GIF

client = redgifs.API().login()

def download_gif(url: yarl.URL, quality: str, folder: Optional[str]):
    id = url.path.split('/')[-1]
    gif = client.get_gif(id)
    gif_url = gif.urls.sd if quality == 'sd' else gif.urls.hd
    filename = f'{gif_url.split("/")[3].split(".")[0]}.mp4'
    click.echo(f'Downloading {id}...')
    if folder:
        client.download(gif_url, f'{folder}/{filename}')
    else:
        client.download(gif_url, f'{filename}')
    click.echo('Download complete.')

def _dl_with_args(gif: GIF, quality: str, folder: Optional[str]):
    gif_url = gif.urls.sd if quality == 'sd' else gif.urls.hd
    filename = f'{gif_url.split("/")[3].split(".")[0]}.mp4'
    if folder:
        client.download(gif_url, f'{folder}/{filename}')
    else:
        client.download(gif_url, f'{filename}')

def download_users_gifs(url: yarl.URL, quality: str, folder: Optional[str]):
    match = re.match(r'https://(www\.)?redgifs\.com\/users\/(?P<username>\w+)', str(url))
    if not match:
        click.UsageError(f'Not a valid redgifs user URL: {url}')
        exit(1)

    user = match.groupdict()['username']
    data = client.search_creator(user)
    curr_page = data.page
    total_pages = data.pages
    total_gifs_in_page = data.gifs
    total = data.total
    done = 0

     # Case where there is only 1 page
    if curr_page == total_pages:
        for gif in total_gifs_in_page:
            try:
                _dl_with_args(gif, quality, folder)
                done += 1
                click.echo(f'Downloaded {done}/{total} GIFs')
            except Exception as e:
                if isinstance(e, FileNotFoundError):
                    click.UsageError(f'[!] An error occured while downloading: {e}\nMake sure you have a folder called "{folder}" in the current directory.')
                    exit(1)
                else:
                    click.UsageError(f'[!] Error occurred when downloading {url}:\n{e}. Continuing...')
                    continue
        click.echo(f'\nDownloaded {done}/{total} videos of "{user}" {f"to {folder} folder" if folder else ""} sucessfully')

    # Case where there is more than 1 page
    while curr_page <= total_pages:
        for gif in total_gifs_in_page:
            try:
                _dl_with_args(gif, quality, folder)
                done += 1
                click.echo(f'Downloaded {done}/{total} GIFs')
            except Exception as e:
                if isinstance(e, FileNotFoundError):
                    click.UsageError(f'[!] An error occured while downloading: {e}\nMake sure you have a folder called "{folder}" in the current working directory.')
                    exit(1)
                else:
                    click.echo(f'[!] Error occurred when downloading {url}:\n{e}. Continuing...')
                    continue

        # If we are in the last page, break the loop
        if curr_page == total_pages:
            break

        curr_page += 1
        total_gifs_in_page.clear()
        data = client.search_creator(user, page=curr_page)
        total_gifs_in_page.extend(data.gifs)

    click.echo(f'\nDownloaded {done}/{total} videos of "{user}" {f"to {folder} folder" if folder else ""} sucessfully')

@click.command()
@click.argument('urls', nargs=-1)
@click.option('-q', '--quality', type=click.Choice(['sd', 'hd']), default='hd', show_default=True, help='Video quality of GIF to download.')
@click.option('--use-dir', 'folder', help='The folder/directory to save the downloads to.', metavar='FOLDER_NAME')
@click.option('--file', help='Download URLs from a newline seperated txt file.', type=click.Path(exists=True))
@click.pass_context
def cli(ctx: click.Context, urls: Iterable[str], quality: str, folder: Optional[str], file: Optional[str]) -> None:
    if not urls and not file:
        click.echo(ctx.command.get_help(ctx))

    if file:
        with open(file) as f:
            [download_gif(url, quality, folder) for url in [yarl.URL(line) for line in f.readlines()]]

    for url in urls:
        url = yarl.URL(url)
        if 'redgifs' not in str(url.host):
            click.UsageError(f'"{url}" is not a valid redgifs URL').show()
            exit(1)

        # Handle 'normal' URLs, i.e, a direct link from browser (eg: "https://redgifs.com/watch/deeznuts")
        if '/watch/' in url.path:
            download_gif(url, quality, folder)

        # Handle /users/ URLs (eg: https://redgifs.com/users/redgifs)
        if '/users/' in url.path:
            download_users_gifs(url, quality, folder)
