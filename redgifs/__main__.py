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

import re
import sys
import platform
import itertools
from pathlib import Path
from typing import Iterable, Optional, TYPE_CHECKING

import click
import yarl

import redgifs
from redgifs.enums import MediaType
from . import __version__

if TYPE_CHECKING:
    from redgifs import API
    from redgifs.models import GIF, Image


def download_gif(client: API, url: yarl.URL, quality: str, folder: Optional[Path], *, skip_check: bool = False):
    # If skip_check is true then this will be the GIF's ID and splitting the URL is not required
    id = str(url).lower() if skip_check else url.path.split('/')[-1]
    click.echo(f'Downloading {id}...')
    gif = client.get_gif(id)
    gif_url = gif.urls.sd if quality == 'sd' else (gif.urls.hd or gif.urls.sd)
    filename = f'{gif_url.split("/")[3].split(".")[0]}.mp4'
    dir_ = f'{folder}/{filename}' if folder else filename
    client.download(gif_url, dir_)
    click.echo('Download complete.')


def _dl_with_args(client: API, gif: GIF | Image, quality: str, folder: Optional[Path], is_image: bool):
    gif_url = gif.urls.sd if quality == 'sd' else gif.urls.hd or gif.urls.sd
    filename = f'{gif_url.split("/")[3].split(".")[0]}.mp4'
    if is_image:
        name, ext = gif_url.split('/')[3].split('.')
        filename = f'{name}.{ext}'

    if folder:
        client.download(gif_url, f'{folder}/{filename}')
    else:
        client.download(gif_url, f'{filename}')


def download_users_gifs(client: API, url: yarl.URL, quality: str, folder: Optional[Path], images_only: bool):
    match = re.match(r'https://(www\.)?redgifs\.com\/users\/(?P<username>\w+)', str(url))
    if not match:
        click.UsageError(f'Not a valid redgifs user URL: {url}')
        exit(1)

    is_image = images_only
    user = match.groupdict()['username']

    media_type = MediaType.IMAGE if is_image else MediaType.GIF
    data = client.search_creator(user, type=media_type)

    curr_page = data.page
    total_pages = data.pages
    media_items = data.images if is_image else data.gifs
    total = data.total
    done = 0

    spinner = itertools.cycle(['-', '\\', '|', '/'])

    while curr_page <= total_pages:
        for item in media_items:
            try:
                _dl_with_args(client, item, quality, folder, is_image)
                done += 1
                click.echo(f'\r{next(spinner)} Downloading {done}/{total} {"images" if is_image else "GIFs"}...', nl=False)
            except Exception as e:
                click.echo(f'[!] An error occurred when downloading {url}: {e}\nContinuing...')
                continue

        if curr_page == total_pages:
            break

        curr_page += 1
        data = client.search_creator(user, page=curr_page, type=media_type)
        media_items = data.images if is_image else data.gifs

    folder_info = f"to folder '{folder}'" if folder else ''
    click.echo(
        f'\r[-] Downloaded {done}/{total} {"images" if is_image else "GIFs"} of user {user} {folder_info} successfully!'
    )


@click.command()
@click.argument('urls', nargs=-1)
@click.option('-v', '--version', is_flag=True, help='Shows currently installed version.')
@click.option(
    '-q',
    '--quality',
    type=click.Choice(['sd', 'hd']),
    default='hd',
    show_default=True,
    help='Video quality of GIF to download.',
)
@click.option(
    '-f',
    '--folder',
    help='The folder to save the downloads to.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    metavar='FOLDER_NAME',
)
@click.option(
    '-i',
    '--input',
    'file',
    help='Download URLs from a newline seperated txt file.',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    metavar='FILE_NAME',
)
@click.option('--images', is_flag=True, help='Download only images from a user profile.')
@click.pass_context
def cli(
    ctx: click.Context,
    urls: Iterable[str],
    quality: str,
    folder: Optional[Path],
    file: Optional[str],
    version: bool,
    images: bool,
) -> None:
    if version:
        info = []
        info.append('- python: v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))
        info.append('- redgifs: v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(redgifs.version_info))
        info.append('- system info: {0.system} {0.release} {0.version}'.format(platform.uname()))
        return click.echo('\n'.join(info))

    if not urls and not file:
        return click.echo(ctx.command.get_help(ctx))

    client = redgifs.API().login()

    if file:
        with open(file) as f:
            [download_gif(client, url, quality, folder) for url in [yarl.URL(line) for line in f.readlines()]]

    for url in urls:
        url = yarl.URL(url)
        if 'redgifs' not in str(url.host):
            download_gif(client, url, quality, folder, skip_check=True)

        # Handle 'normal' URLs, i.e, a direct link (eg: "https://redgifs.com/watch/deeznuts")
        if '/watch/' in url.path:
            download_gif(client, url, quality, folder)

        # Handle /users/ URLs (eg: https://redgifs.com/users/redgifs)
        if '/users/' in url.path:
            download_users_gifs(client, url, quality, folder, images)
