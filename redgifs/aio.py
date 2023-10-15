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

import io
import os
from typing import Any, Dict, List, Optional, Union

import aiohttp

from .http import AsyncHttp, ProxyAuth
from .tags import Tags
from .enums import Order
from .utils import _to_web_url, _async_read_tags_json, build_file_url, _gifs_iter, _images_iter
from .parser import parse_feeds, parse_search, parse_creator, parse_creators, parse_search_image
from .models import GIF, URL, CreatorResult, Feeds, Image, SearchResult, CreatorsResult

class API:
    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        *,
        proxy: Optional[str] = None,
        proxy_auth: Optional[ProxyAuth] = None
    ) -> None:
        self.http: AsyncHttp = AsyncHttp(session, proxy=proxy, proxy_auth=proxy_auth)
        self._tags = Tags()

    async def login(self) -> 'API':
        await self.http.login()
        return self

    async def get_feeds(self) -> Feeds:
        feeds = await self.http.get_feeds()
        return parse_feeds(feeds)

    async def get_tags(self) -> List[Dict[str, Union[str, int]]]:
        resp = await self.http.get_tags()
        return resp['tags']

    async def get_gif(self, id: str) -> GIF:
        json: Dict[str, Any] = (await self.http.get_gif(id))['gif']
        urls = json['urls']
        return GIF(
            id=json['id'],
            create_date=json['createDate'],
            has_audio=json['hasAudio'],
            width=json['width'],
            height=json['height'],
            likes=json['likes'],
            tags=json['tags'],
            verified=json['verified'],
            views=json['views'],
            duration=json['duration'],
            published=json['published'],
            urls=URL(
                sd=urls['sd'],
                hd=urls['hd'],
                poster=urls['poster'],
                thumbnail=urls['thumbnail'],
                vthumbnail=urls.get('vthumbnail'),
                web_url=_to_web_url(json['id']),
                file_url=build_file_url(urls['sd'])
            ),
            username=json['userName'],
            type=json['type'],
            avg_color=json['avgColor'],
        )

    async def get_trending_tags(self) -> List[Dict[str, Union[str, int]]]:
        result = (await self.http.get_trending_tags())['tags']
        return result

    async def get_trending_gifs(self) -> List[GIF]:
        r = (await self.http.get_trending_gifs())['gifs']
        return _gifs_iter(r)

    async def get_trending_images(self) -> List[Image]:
        r = (await self.http.get_trending_images())['gifs']
        return _images_iter(r)

    async def fetch_tag_suggestions(self, query: str) -> List[str]:
        result = await self.http.get_tag_suggestions(query)
        return [d['text'] for d in result]

    async def search(
        self,
        search_text: str,
        *,
        order: Order = Order.trending,
        count: int = 80,
        page: int = 1
    ) -> SearchResult:
        if len(self._tags.tags_mapping) == 0:
            tags = await _async_read_tags_json()
            self._tags._set(tags)

        st = self._tags.search(search_text)[0]
        resp = await self.http.search(st, order, count, page)
        return parse_search(st, resp)

    search_gif = search

    async def search_creators(
        self,
        *,
        page: int = 1,
        order: Order = Order.recent,
        verified: bool = False,
        tags: Optional[List[str]] = None
    ) -> CreatorsResult:
        resp = await self.http.search_creators(page=page, order=order, verified=verified, tags=tags)
        return parse_creators(resp)

    async def search_creator(
        self,
        username: str,
        *,
        page: int = 1,
        count: int = 80,
        order: Order = Order.recent
    ) -> CreatorResult:
        resp = await self.http.search_creator(username=username, page=page, count=count, order=order)
        return parse_creator(resp)

    search_user = search_creator

    async def search_image(
        self,
        search_text: str,
        *,
        order: Order = Order.new,
        count: int = 80,
        page: int = 1
    ) -> SearchResult:
        # We are not going to use Tags.search() here because it doesn't matter
        # whatever the search_text is, this API endpoints provides images nonetheless.
        resp = await self.http.search_image(search_text, order, count, page)
        return parse_search_image(search_text, resp)

    async def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]) -> int:
        return (await self.http.download(url, fp))

    async def close(self) -> None:
        return (await self.http.close())
