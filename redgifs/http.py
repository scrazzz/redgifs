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

import typing
from urllib.parse import quote
from typing import Any, ClassVar, List, Literal, Optional, Union

import requests
import aiohttp

from .errors import HTTPException
from .enums import Tags, Order

class Route:
    BASE: ClassVar[str] = "https://api.redgifs.com"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        url: str = self.BASE + self.path
        if parameters:
            url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url

class HTTP:
    def __init__(self) -> None:
        self.__session: requests.Session = requests.Session()

    def request(self, route: Route, **kwargs: Any):
        url: str = route.url
        method: str = route.method
        r: requests.Response = self.__session.request(method, url, **kwargs)
        js = r.json()
        if r.status_code == 200:
            return js
        else:
            raise HTTPException(r, js)

    def get_tags(self, **params: Any):
        return self.request(Route('GET', '/v1/tags'))
    
    def search(self, search_text: Union[str, Tags], order: Order, count: int, page: int, **params: Any):
        r = Route(
            'GET',
            '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)

    def search_creators(self, page: int, order: Order, verified: bool, tags: Union[List[Tags], List[str], None], **params: Any):
        if tags:
            r = Route(
                'GET',
                '/v1/creators/search?page={page}&order={order}&verified={verified}&tags={tags}',
                page=page, order=order.value, verified=verified, tags=','.join(t.value for t in tags) if isinstance(tags[0], Tags) else ','.join(t for t in tags) # type: ignore
            )
        else:
            r = Route(
                'GET',
                '/v1/creators/search?page={page}&order={order}&verified={verified}',
                page=page, order=order.value, verified=verified
            )
        return self.request(r, **params)

    def get_gif(self, id: str, **params: Any):
        r = Route(
            'GET',
            '/v2/gifs/{id}',
            id=id
        )
        return self.request(r, **params)

    def close(self) -> None:
        self.__session.close()

class AsyncHttp(HTTP):
    def __init__(self) -> None:
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession()

    async def request(self, route: Route, **kwargs: Any):
        url: str = route.url
        method: str = route.method
        async with self.__session.request(method, url, **kwargs) as resp:
            js = await resp.json()
            if resp.status == 200:
                return js
            else:
                raise HTTPException(resp, js, _async=True)

    async def close(self):
        await self.__session.close()
