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

import re
import json
import pkgutil
import asyncio
from datetime import datetime
from typing import Any, Dict, List

import yarl

from .models import GIF, URL, Image, User
from .const import REDGIFS_THUMBS_RE

def _to_web_url(id_or_url: str, use_regex: bool = False) -> str:
    if not use_regex:
        return f'https://redgifs.com/watch/{id_or_url.lower()}'

    match = re.match(REDGIFS_THUMBS_RE, id_or_url)
    if not match:
        return ''

    try:
        id = match.group('id')
        return f'https://redgifs.com/watch/{id.lower()}'
    except IndexError:
        return ''

def strip_ip(url: str) -> str:
    u = yarl.URL(url)
    if u.query.get('for'):
        return str(u % {'for': 'REDACTED'})
    return url

def build_file_url(url: str) -> str:
    # use the 'sd' url here
    u = yarl.URL(url)
    filename = u.path.replace('/', '').replace('-mobile.mp4', '')
    return f'https://api.redgifs.com/v2/gifs/{filename.lower()}/files/{filename}.mp4'

def _read_tags_json() -> Dict[str, str]:
    file_ = pkgutil.get_data(__name__, 'tags.json') # type: ignore - We know this won't be None
    return json.loads(file_) # type: ignore - same reason above

async def _async_read_tags_json() -> Dict[str, str]:
    r = await asyncio.get_event_loop().run_in_executor(None, _read_tags_json)
    return r

def _gifs_iter(gifs: List[Dict[str, Any]]) -> List[GIF]:
    return [
        GIF(
            id=g['id'],
            create_date=datetime.utcfromtimestamp(g['createDate']),
            has_audio=g['hasAudio'],
            width=g['width'],
            height=g['height'],
            likes=g['likes'],
            tags=g['tags'],
            verified=g['verified'],
            views=g['views'],
            duration=int(g['duration']) if g['duration'] is not None else g['duration'],
            published=g['published'],
            urls=URL(
                sd=g['urls']['sd'],
                hd=g['urls']['hd'],
                poster=g['urls']['poster'],
                thumbnail=g['urls']['thumbnail'],
                vthumbnail=g['urls']['vthumbnail'],
                web_url=_to_web_url(g['id']),
                file_url=build_file_url(g['urls']['sd'])
            ),
            username=g['userName'],
            type=g['type'],
            avg_color=g['avgColor'],
        )
        for g in gifs
    ]

def _images_iter(images: List[Dict[str, Any]]) -> List[Image]:
    return [
        Image(
            id=i['id'],
            create_date=datetime.utcfromtimestamp(i['createDate']),
            width=i['width'],
            height=i['height'],
            likes=i['likes'],
            tags=i['tags'],
            verified=i['verified'],
            views=i['views'],
            published=i['published'],
            urls=URL(
                sd=i['urls']['sd'],
                hd=i['urls']['hd'],
                poster=i['urls']['poster'],
                thumbnail=i['urls']['thumbnail'],
                vthumbnail=i['urls']['vthumbnail'],
                web_url=_to_web_url(i['id']),
                file_url=None
            ),
            username=i['userName'],
            type=i['type'],
            avg_color=i['avgColor'],
        )
        for i in images
    ]

def _users_iter(users: List[Dict[str, Any]]) -> List[User]:
    return [
        User(
            # I only had this occurrence once where redgifs did not
            # send the response properly and messed up the entire JSON
            # response, this is why I have used dict.get() here.
            creation_time=datetime.utcfromtimestamp(user.get('creationtime')) if user.get('creationtime') is not None else None, # type: ignore
            description=user.get('description'),
            followers=user.get('followers'),
            following=user.get('following'),
            gifs=user.get('gifs'),
            name=user.get('name'),
            profile_image_url=user.get('profileImageUrl'),
            profile_url=user.get('profileUrl'),
            published_collections=user.get('publishedCollections'),
            status=user.get('status'),
            published_gifs=user.get('publishedGifs'),
            subscription=user.get('subscription'),
            url=user.get('url'),
            username=user.get('username'),
            verified=user.get('verified'),
            views=user.get('views'),
            poster=user.get('poster'),
            preview=user.get('preview'),
            thumbnail=user.get('thumbnail'),
            links=user.get('links')
        )
        for user in users
    ]
