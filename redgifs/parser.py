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

from typing import List

from .models import SearchResult, Gifs, URLs, Users

# might not even use this tbh
def parse_search(json: dict):
    json_gifs = json['gifs']
    users = json['users']
    return SearchResult(
        page=json['page'],
        pages=json['pages'],
        total=json['total'],
        gifs=[
            Gifs(
                id=gif['id'],
                create_date=gif['createDate'].
                has_audio=gif['hasAudio'],
                width=gif['width'],
                height=gif['height'],
                likes=gif['likes'],
                tags=gif['tags'],
                verified=gif['verified'],
                views=gif['views'],
                duration=gif['duration'],
                published=gif['published'],
                urls=URLs(
                    sd=gif['urls']['sd'],
                    hd=gif['urls']['hd'],
                    poster=gif['urls']['poster'],
                    thumbnail=gif['urls']['thumbnail'],
                    vthumbnail=gif['urls']['vthumbnail']
                )
                username=gif['userName'],
                type=gif['type'],
                avg_color=gif['avgColor']
            ) for gif in json_gifs],
        users=[
            Users(
                creation_time=user['creationtime'],
                description=user['description'],
                followers=user['followers'],
                following=user['following'],
                gifs=user['gifs'],
                name=user['name'],
                profile_image_url=user['profileImageUrl'],
                profile_url=user['profileUrl'],
                published_collections=user['publishedCollections'],
                published_gifs=user['publishedGifs'],
                subscription=user['subscription'],
                url=user['url'],
                username=user['username'],
                verified=user['verified'],
                views=user['views'],
                poster=user['poster'],
                preview=user['preview'],
                thumbnail=user['thumbnail']
            )
            for user in users
        ],
        tags=json['tags']
    )


def parse_search_creators(json: dict):
    ...