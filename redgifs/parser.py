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

import logging
from datetime import datetime
from typing import Any, Dict

from .utils import _to_web_url, _gifs_iter, _images_iter, _users_iter, build_file_url
from .models import GIF, URL, CreatorResult, Feeds, Image, User, SearchResult, CreatorsResult

_log = logging.getLogger(__name__)

def parse_feeds(json: Dict[str, Any]) -> Feeds:
    _log.debug('Parsing feeds')
    hgifs = json['horizontalGifs']
    vgifs = json['verticalGifs']
    hotcreators = json['hotCreators']
    newcreators = json['newCreators']
    longgifs = json['longGifs']
    verifiedgifs = json['verifiedGifs']
    soundgifs = json['soundGifs']
    hotgifs = json['hotGifs']
    hotimages = json['hotImages']
    verifiedimages = json['verifiedImages']
    return Feeds(
        horizontal_gifs=_gifs_iter(hgifs),
        vertical_gifs=_gifs_iter(vgifs),
        hot_creators=_users_iter(hotcreators),
        new_creators=_users_iter(newcreators),
        long_gifs=_gifs_iter(longgifs),
        verified_gifs=_gifs_iter(verifiedgifs),
        sound_gifs=_gifs_iter(soundgifs),
        hot_gifs=_gifs_iter(hotgifs),
        hot_images=_images_iter(hotimages),
        verified_images=_images_iter(verifiedimages),
    )

# For GIFs
def parse_search(searched_for: str, json: Dict[str, Any]) -> SearchResult:
    _log.debug('Using `parse_search` for: {searched_for}')
    json_gifs = json['gifs']
    users = json['users']
    return SearchResult(
        searched_for=searched_for,
        page=json['page'],
        pages=json['pages'],
        total=json['total'],
        images=None,
        gifs=[
            GIF(
                id=gif['id'],
                create_date=datetime.utcfromtimestamp(gif['createDate']),
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
                    hd=gif['urls']['hd'],
                    poster=gif['urls']['poster'],
                    thumbnail=gif['urls']['thumbnail'],
                    vthumbnail=gif['urls']['vthumbnail'],
                    web_url=_to_web_url(gif['id']),
                    file_url=build_file_url(gif['urls']['sd'])
                ),
                username=gif['userName'],
                type=gif['type'],
                avg_color=gif['avgColor'],
            )
            for gif in json_gifs
        ],
        users=[
            User(
                # I only had this occurrence once where redgifs did not
                # send the response properly and messed up the entire JSON
                # response, this is why I have used dict.get() here.
                creation_time=datetime.utcfromtimestamp(user.get('creationtime'))
                if user.get('creationtime') is not None else None,
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
                links=user.get('links'),
            )
            for user in users
        ],
        tags=json['tags'],
    )

# For images
def parse_search_image(searched_for: str, json: Dict[str, Any]) -> SearchResult:
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
                create_date=datetime.utcfromtimestamp(gif['createDate']),
                width=gif['width'],
                height=gif['height'],
                likes=gif['likes'],
                tags=gif['tags'],
                verified=gif['verified'],
                views=gif['views'],
                published=gif['published'],
                urls=URL(
                    sd=gif['urls']['sd'],
                    hd=gif['urls']['hd'],
                    poster=gif['urls']['poster'],
                    thumbnail=gif['urls']['thumbnail'],
                    vthumbnail=gif['urls']['vthumbnail'],
                    web_url=_to_web_url(gif['id']),
                    file_url=None
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

def parse_creators(json: Dict[str, Any]) -> CreatorsResult:
    _log.debug('Using `parse_creators`')
    items = json['items']
    return CreatorsResult(
        items=_users_iter(items),
        pages=json['pages'],
        page=json['page'],
        total=json['total'],
    )

def parse_creator(json: Dict[str, Any]) -> CreatorResult:
    _log.debug('Using `parse_creator`')
    user = json['users'][0]
    return CreatorResult(
        creator=User(
            creation_time=datetime.utcfromtimestamp(user['creationtime']),
            description=user['description'],
            followers=user['followers'],
            following=user['following'],
            gifs=json['gifs'],
            name=user['name'],
            profile_image_url=user['profileImageUrl'],
            profile_url=user['profileUrl'],
            published_collections=user['publishedCollections'],
            status=user['status'],
            published_gifs=user['publishedGifs'],
            subscription=user['subscription'],
            url=user['url'],
            username=user['username'],
            verified=user['verified'],
            views=user['views'],
            poster=user['poster'],
            preview=user['preview'],
            thumbnail=user['thumbnail'],
            links=user.get('links'),
        ),
        page=json['page'],
        pages=json['pages'],
        total=json['total'],
        gifs=[
            GIF(
                id=gif['id'],
                create_date=datetime.utcfromtimestamp(gif['createDate']),
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
                    hd=gif['urls']['hd'],
                    poster=gif['urls']['poster'],
                    thumbnail=gif['urls']['thumbnail'],
                    vthumbnail=gif['urls']['vthumbnail'],
                    web_url=_to_web_url(gif['id']),
                    file_url=build_file_url(gif['urls']['sd'])
                ),
                username=gif['userName'],
                type=gif['type'],
                avg_color=gif['avgColor'],
            )
            for gif in json['gifs']
        ]
    )
