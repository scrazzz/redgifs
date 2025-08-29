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

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from .enums import MediaType
from .errors import RedGifsError
from .utils import _users_iter, build_file_url, to_embed_url, to_web_url
from .models import GIF, URL, CreatorResult, Image, User, SearchResult, CreatorsResult

if TYPE_CHECKING:
    from redgifs.types.gif import GifResponse
    from redgifs.types.image import ImageResponse
    from redgifs.types.user import CreatorResponse, CreatorsResponse

_log = logging.getLogger(__name__)


# For GIFs
def parse_search(searched_for: str, json: GifResponse, media_type: MediaType) -> SearchResult:
    _log.debug('Using `parse_search` for: {searched_for}')
    json_gifs = json['gifs']
    users = json['users']
    return SearchResult(
        searched_for=searched_for,
        page=json['page'],
        pages=json['pages'],
        total=json['total'],
        images=[
            Image(
                id=img['id'],
                create_date=datetime.fromtimestamp(img['createDate'], tz=timezone.utc),
                width=img['width'],
                height=img['height'],
                likes=img['likes'],
                tags=img['tags'],
                verified=img['verified'],
                views=img['views'],
                published=img['published'],
                urls=URL(
                    sd=img['urls']['sd'],
                    hd=img['urls'].get('hd'),
                    poster=img['urls'].get('poster'),
                    thumbnail=img['urls'].get('thumbnail'),
                    vthumbnail=img['urls'].get('vthumbnail'),
                    web_url=to_web_url(img['id']),
                    file_url=None,
                    embed_url=to_embed_url(img['urls'].get('hd') or img['urls']['sd']),
                ),
                username=img['userName'],
                type=img['type'],
                avg_color=img['avgColor'],
            )
            for img in json['gifs']
            if media_type == MediaType.IMAGE
        ],
        gifs=[
            GIF(
                id=gif['id'],
                create_date=datetime.fromtimestamp(gif['createDate'], tz=timezone.utc),
                has_audio=gif['hasAudio'],
                width=gif['width'],
                height=gif['height'],
                likes=gif['likes'],
                tags=gif['tags'],
                verified=gif['verified'],
                views=gif['views'],
                duration=int(gif['duration']) if gif['duration'] is not None else gif['duration'],
                published=gif['published'],
                urls=URL(
                    sd=gif['urls']['sd'],
                    hd=gif['urls'].get('hd'),
                    poster=gif['urls'].get('poster'),
                    thumbnail=gif['urls'].get('thumbnail'),
                    vthumbnail=gif['urls'].get('vthumbnail'),
                    web_url=to_web_url(gif['id']),
                    file_url=build_file_url(gif['urls']['sd']),
                    embed_url=to_embed_url(gif['urls']['sd']),
                ),
                username=gif['userName'],
                type=gif['type'],
                avg_color=gif['avgColor'],
            )
            for gif in json_gifs
            if media_type == MediaType.GIF
        ],
        users=[
            User(
                creation_time=datetime.fromtimestamp(user.get('creationtime'), tz=timezone.utc)
                if user.get('creationtime') is not None
                else None,
                description=user.get('description'),
                followers=user['followers'],
                following=user['following'],
                gifs=user['gifs'],
                name=user.get('name'),
                profile_image_url=user.get('profileImageUrl'),
                profile_url=user.get('profileUrl'),
                published_collections=user.get('publishedCollections'),
                status=user.get('status'),
                published_gifs=user['publishedGifs'],
                subscription=user['subscription'],
                url=user['url'],
                username=user['username'],
                verified=user['verified'],
                views=user['views'],
                poster=user.get('poster'),
                preview=user.get('preview'),
                thumbnail=user.get('thumbnail'),
                links=user.get('links'),
            )
            for user in users
        ],
        tags=json['tags'],
    )


# For images
def parse_search_image(searched_for: str, json: ImageResponse) -> SearchResult:
    _log.debug('Using `parse_search` for: {searched_for}')
    json_gifs = json['gifs']
    users = json['users']
    return SearchResult(
        searched_for=searched_for,
        page=json['page'],
        pages=json['pages'],
        total=json['total'],
        gifs=None,
        images=[
            Image(
                id=gif['id'],
                create_date=datetime.fromtimestamp(gif['createDate'], tz=timezone.utc),
                width=gif['width'],
                height=gif['height'],
                likes=gif['likes'],
                tags=gif['tags'],
                verified=gif['verified'],
                views=gif['views'],
                published=gif['published'],
                urls=URL(
                    sd=gif['urls']['sd'],
                    hd=gif['urls'].get('hd'),
                    poster=gif['urls'].get('poster'),
                    thumbnail=gif['urls'].get('thumbnail'),
                    vthumbnail=gif['urls'].get('vthumbnail'),
                    web_url=to_web_url(gif['id']),
                    file_url=None,
                    embed_url=gif['urls'].get('hd'),
                ),
                username=gif['userName'],
                type=gif['type'],
                avg_color=gif['avgColor'],
            )
            for gif in json_gifs
        ],
        users=_users_iter(users),
        tags=json['tags'],
    )


def parse_creators(json: CreatorsResponse) -> CreatorsResult:
    _log.debug('Using `parse_creators`')
    items = json['items']
    return CreatorsResult(
        items=_users_iter(items),
        pages=json['pages'],
        page=json['page'],
        total=json['total'],
    )


def parse_creator(json: CreatorResponse, media_type: MediaType) -> CreatorResult:
    _log.debug('Using `parse_creator`')

    # RedGifs API should actually throw a 404 HTTP response if the user is not found
    # BUT since it does NOT do that everytime, this is how we are going to handle it.
    if len(json['users']) == 0:
        raise RedGifsError('User not found')

    user = json['users'][0]
    return CreatorResult(
        creator=User(
            creation_time=datetime.fromtimestamp(user['creationtime'], tz=timezone.utc),
            description=user['description'],
            followers=user['followers'],
            following=user['following'],
            gifs=user['gifs'],
            name=user.get('name'),
            profile_image_url=user['profileImageUrl'],
            profile_url=user.get('profileUrl'),
            published_collections=user['publishedCollections'],
            status=user.get('status'),
            published_gifs=user['publishedGifs'],
            subscription=user['subscription'],
            url=user['url'],
            username=user['username'],
            verified=user['verified'],
            views=user['views'],
            poster=user.get('poster'),
            preview=user.get('preview'),
            thumbnail=user.get('thumbnail'),
            links=user.get('links'),
        ),
        page=json['page'],
        pages=json['pages'],
        total=json['total'],
        gifs=[
            GIF(
                id=gif['id'],
                create_date=datetime.fromtimestamp(gif['createDate'], tz=timezone.utc),
                has_audio=gif['hasAudio'],  # type: ignore - We aren't setting values for ImageInfo
                width=gif['width'],
                height=gif['height'],
                likes=gif['likes'],
                tags=gif['tags'],
                verified=gif['verified'],
                views=gif['views'],
                duration=gif['duration'],  # type: ignore - We aren't setting values for ImageInfo
                published=gif['published'],
                urls=URL(
                    sd=gif['urls']['sd'],
                    hd=gif['urls'].get('hd'),
                    poster=gif['urls'].get('poster'),
                    thumbnail=gif['urls'].get('thumbnail'),
                    vthumbnail=gif['urls'].get('vthumbnail'),
                    web_url=to_web_url(gif['id']),
                    file_url=build_file_url(gif['urls']['sd']),
                    embed_url=to_embed_url(gif['urls']['sd']),
                ),
                username=gif['userName'],
                type=gif['type'],
                avg_color=gif['avgColor'],
            )
            for gif in json['gifs']
            if media_type == MediaType.GIF
        ],
        images=[
            Image(
                id=img['id'],
                create_date=datetime.fromtimestamp(img['createDate'], tz=timezone.utc),
                width=img['width'],
                height=img['height'],
                likes=img['likes'],
                tags=img['tags'],
                verified=img['verified'],
                views=img['views'],
                published=img['published'],
                urls=URL(
                    sd=img['urls']['sd'],
                    hd=img['urls'].get('hd'),
                    poster=img['urls'].get('poster'),
                    thumbnail=img['urls'].get('thumbnail'),
                    vthumbnail=img['urls'].get('vthumbnail'),
                    web_url=to_web_url(img['id']),
                    file_url=None,
                    embed_url=img['urls'].get('hd'),
                ),
                username=img['userName'],
                type=img['type'],
                avg_color=img['avgColor'],
            )
            for img in json['gifs']
            if media_type == MediaType.IMAGE  # RedGifs return the key for this data as "gifs" even though it's an image...
        ],
    )
