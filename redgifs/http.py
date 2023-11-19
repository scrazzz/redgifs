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
import re
import sys
import logging
from urllib.parse import quote
from typing import Any, ClassVar, Dict, List, NamedTuple, Optional, Union

import requests
import aiohttp
import yarl

from . import __version__
from .errors import HTTPException
from .enums import Order
from .const import REDGIFS_THUMBS_RE
from .utils import strip_ip

_log = logging.getLogger(__name__)

class Route:
    BASE: ClassVar[str] = "https://api.redgifs.com"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        url: str = self.BASE + self.path
        if parameters:
            url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url

class ProxyAuth(NamedTuple):
    """
    username: :class:`str`
        The username.
    password: :class:`str`
        The password.
    """
    username: str
    password: str

class HTTP:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        *,
        proxy: Optional[str] = None,
        proxy_auth: Optional[ProxyAuth] = None
    ) -> None:

        if session is not None and not isinstance(session, requests.Session):
            raise RuntimeError("session is not of type requests.Session")

        self.__session: requests.Session = session or requests.Session()
        self.headers: Dict[str, str] = {
            'User-Agent': f'redgifs (https://github.com/scrazzz/redgifs {__version__}) Python/{sys.version[:3]}'
        }
        self.proxy: Optional[yarl.URL] = yarl.URL(proxy) if proxy else None
        self.proxy_auth: Optional[ProxyAuth] = proxy_auth

        # Set proxy
        if self.proxy:
            self._proxy = {self.proxy.scheme: str(self.proxy)}
        else:
            self._proxy = None

        # Set proxy auth
        if self.proxy_auth and self._proxy:
            self._proxy_auth = (self.proxy_auth.username, self.proxy_auth.password)
        else:
            self._proxy_auth = None

    def request(self, route: Route, **kwargs: Any) -> Any:
        url: str = route.url
        method: str = route.method
        r: requests.Response = self.__session.request(
            method, url, headers=self.headers, proxies=self._proxy, auth=self._proxy_auth, timeout=60.0, **kwargs
        )
        _log.debug(f'{method} {url} returned code: {r.status_code}')
        js = r.json()
        if r.status_code == 200:
            _log.debug(f'{method} {url} received: {js}')
            return js
        else:
            raise HTTPException(r, js)

    def close(self) -> None:
        self.__session.close()

    # TODO: Implement OAuth login support
    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        if (username and password) is None:
            temp_token = self.get_temp_token()['token']
            self.headers['authorization'] = f'Bearer {temp_token}'
        else:
            raise NotImplementedError

    def get_temp_token(self):
        return self.request(Route('GET', '/v2/auth/temporary'))

    # GIF methods

    def get_feeds(self):
        return self.request(Route('GET', '/v2/home/feeds'))

    def get_tags(self, **params: Any):
        return self.request(Route('GET', '/v1/tags'), **params)

    def get_gif(self, id: str, **params: Any):
        return self.request(Route('GET', '/v2/gifs/{id}', id=id), **params)

    def search(self, search_text: str, order: Order, count: int, page: int, **params: Any):
        r = Route(
            'GET', '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)
    
    # User/Creator methods

    def search_creators(
        self,
        page: int,
        order: Order,
        verified: bool,
        tags: Optional[List[str]],
        **params: Any
    ):
        url = '/v1/creators/search?page={page}&order={order}'
        if verified:
            url += '&verified={verified}'
        if tags:
            url += '&tags={tags}'
            r = Route(
                'GET', url,
                page=page, order=order.value, verified='y' if verified else 'n',
                tags=','.join(t for t in tags)
            )
            return self.request(r, **params)
        else:
            r = Route(
                'GET', url,
                page=page, order=order.value, verified='y' if verified else 'n'
            )
            return self.request(r, **params)

    def search_creator(self, username: str, page: int, count: int, order: Order, **params):
        r = Route(
            'GET', '/v2/users/{username}/search?page={page}&count={count}&order={order}',
            username=username, page=page, count=count, order=order.value
        )
        return self.request(r, **params)

    def get_trending_gifs(self):
        r = Route('GET', '/v2/explore/trending-gifs')
        return self.request(r)

    # Pic methods

    def search_image(self, search_text: str, order: Order, count: int, page: int, **params: Any):
        r = Route(
            'GET', '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}&type=i',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)

    def get_trending_images(self):
        r = Route('GET', '/v2/explore/trending-images')
        return self.request(r)

    # Tag methods

    def get_trending_tags(self):
        r = Route('GET', '/v2/search/trending')
        return self.request(r)

    def get_tag_suggestions(self, query: str):
        r = Route(
            'GET', '/v2/search/suggest?query={query}',
            query=query
        )
        return self.request(r)

    # download

    def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]) -> int:
        """A friendly method to download a RedGifs media."""

        yarl_url = yarl.URL(url)
        str_url = str(yarl_url)

        if (yarl_url.host and 'redgifs.com' not in yarl_url.host):
            raise TypeError(f'"{strip_ip(str_url)}" is not a valid RedGifs URL')

        def dl(url: str) -> int:
            r = self.__session.get(url, headers = self.headers)
            _log.debug(f'GET {url} returned code: {r.status_code}')

            data = r.content
            if isinstance(fp, io.BufferedIOBase):
                return (fp.write(data))
            else:
                with open(fp, 'wb') as f:
                    return f.write(data)

        # If it's a direct URL
        if all([x in str(yarl_url.host) for x in ['thumbs', 'redgifs']]):
            match = re.match(REDGIFS_THUMBS_RE, str_url)
            if match:
                return (dl(str_url))
            raise TypeError(f'"{strip_ip(str_url)}" is an invalid RedGifs URL.')

        # If it's a 'watch' URL
        if 'watch' in yarl_url.path:
            id = yarl_url.path.strip('/watch/')
            hd_url = self.get_gif(id)['gif']['urls']['hd']
            return (dl(hd_url))

        raise TypeError(f'"{strip_ip(str_url)}" is not a valid RedGifs URL')


class AsyncHttp(HTTP):
    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        *,
        proxy: Optional[str] = None,
        proxy_auth: Optional[ProxyAuth] = None
    ) -> None:

        if session is not None and not isinstance(session, aiohttp.ClientSession):
            raise RuntimeError("session is not of type aiohttp.ClientSession")

        self.__session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self.headers: Dict[str, str] = {
            'User-Agent': f'redgifs (https://github.com/scrazzz/redgifs {__version__}) Python/{sys.version[:3]}'
        }
        self.proxy: Optional[yarl.URL] = yarl.URL(proxy) if proxy else None
        self.proxy_auth: Optional[ProxyAuth] = proxy_auth

        # Set proxy auth
        if self.proxy_auth and self.proxy:
            self._proxy_auth = aiohttp.BasicAuth(self.proxy_auth.username, self.proxy_auth.password)
        else:
            self._proxy_auth = None

    # TODO: Implement OAuth login support
    async def login(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        if (username and password) is None:
            temp_token = await self.get_temp_token()
            self.headers['authorization'] = f'Bearer {temp_token["token"]}'
        else:
            raise NotImplementedError

    async def request(self, route: Route, **kwargs: Any) -> Any:
        url: str = route.url
        method: str = route.method
        async with self.__session.request(
            method, url, headers=self.headers, proxy=str(self.proxy) if self.proxy else None, proxy_auth=self._proxy_auth, **kwargs
        ) as resp:
            _log.debug(f'{method} {url} returned code: {resp.status}')
            js = await resp.json()
            if resp.status == 200:
                _log.debug(f'{method} {url} received: {js}')
                return js
            else:
                raise HTTPException(resp, js)

    async def get_temp_token(self):
        return (await self.request(Route('GET', '/v2/auth/temporary')))

    async def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]) -> int:
        yarl_url = yarl.URL(url)
        str_url = str(yarl_url)

        if (yarl_url.host and 'redgifs.com' not in yarl_url.host):
            raise TypeError(f'"{strip_ip(str_url)}" is not a valid RedGifs URL')

        async def dl(url: str) -> int:
            async with self.__session.get(url, headers = self.headers) as r:
                _log.debug(f'GET {str_url} returned code: {r.status}')

                data = await r.read()
                if isinstance(fp, io.BufferedIOBase):
                    return (fp.write(data))
                else:
                    with open(fp, 'wb') as f:
                        return f.write(data)

        # If it's a direct URL
        if all([x in str(yarl_url.host) for x in ['thumbs', 'redgifs']]):
            match = re.match(REDGIFS_THUMBS_RE, str_url)
            if match:
                return (await dl(str_url))
            raise TypeError(f'"{strip_ip(str_url)}" is an invalid RedGifs URL.')

        # If it's a 'watch' URL
        if 'watch' in yarl_url.path:
            id = yarl_url.path.strip('/watch/')
            hd_url = (await self.get_gif(id))['gif']['urls']['hd']
            return (await dl(hd_url))

        raise TypeError(f'"{strip_ip(str_url)}" is not a valid RedGifs URL')

    async def close(self) -> None:
        await self.__session.close()
