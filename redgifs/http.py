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
import sys
import logging
from urllib.parse import quote
from typing import TYPE_CHECKING, Any, ClassVar, Coroutine, Dict, List, NamedTuple, Optional, TypeVar, Union

import requests
import aiohttp
import yarl

from . import __version__
from .errors import HTTPException
from .enums import Order, MediaType
from .utils import strip_ip

__all__ = ('ProxyAuth',)

_log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from redgifs.types.gif import GetGifResponse, GifResponse
    from redgifs.types.image import ImageResponse, TrendingImagesResponse
    from redgifs.types.tags import TagsResponse, TagSuggestion
    from redgifs.types.user import CreatorResponse, CreatorsResponse

    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]

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

        if session is not None and session is not isinstance(session, requests.Session):
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
    def login(self, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None) -> None:
        if token is not None:
            self.headers['authorization'] = f'Bearer {token}'
        elif (username and password) is None:
            temp_token = self.get_temp_token()['token']
            self.headers['authorization'] = f'Bearer {temp_token}'
        else:
            raise NotImplementedError

    def get_temp_token(self):
        return self.request(Route('GET', '/v2/auth/temporary'))

    # GIF methods

    def get_tags(self, **params: Any) -> TagsResponse:
        return self.request(Route('GET', '/v1/tags'), **params)

    def get_gif(self, id: str, **params: Any) -> GetGifResponse:
        return self.request(Route('GET', '/v2/gifs/{id}', id=id), **params)

    def search(self, search_text: str, order: Order, count: int, page: int, **params: Any) -> GifResponse:
        r = Route(
            'GET', '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)

    def get_top_this_week(self, count: int, page: int, type: MediaType, **params) -> GifResponse:
        r = Route(
            'GET', '/v2/gifs/search?order=top7&count={count}&page={page}&type={type}',
            count=count, page=page, type=type.value
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
    ) -> CreatorsResponse:
        url = '/v1/creators/search?page={page}&order={order}'
        if verified:
            url += '&verified={verified}'
        if tags:
            url += '&tags={tags}'
            r = Route(
                'GET', url,
                page=page, order=order.value, verified='y' if verified else 'n', tags=','.join(t for t in tags)
            )
            return self.request(r, **params)
        else:
            r = Route(
                'GET', url,
                page=page, order=order.value, verified='y' if verified else 'n'
            )
            return self.request(r, **params)

    def search_creator(self, username: str, page: int, count: int, order: Order, type: MediaType, **params) -> CreatorResponse:
        r = Route(
            'GET', '/v2/users/{username}/search?page={page}&count={count}&order={order}&type={type}',
            username=username, page=page, count=count, order=order.value, type=type.value
        )
        return self.request(r, **params)

    def get_trending_gifs(self) -> GifResponse:
        r = Route('GET', '/v2/explore/trending-gifs')
        return self.request(r)

    # Pic methods

    def search_image(self, search_text: str, order: Order, count: int, page: int, **params: Any) -> ImageResponse:
        r = Route(
            'GET', '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}&type=i',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)

    def get_trending_images(self) -> TrendingImagesResponse:
        r = Route('GET', '/v2/explore/trending-images')
        return self.request(r)

    # Tag methods

    def get_trending_tags(self) -> TagsResponse:
        r = Route('GET', '/v2/search/trending')
        return self.request(r)

    def get_tag_suggestions(self, query: str) -> List[TagSuggestion]:
        r = Route('GET', '/v2/search/suggest?query={query}', query=query)
        return self.request(r)

    # download

    def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]) -> Union[Coroutine[Any, Any, int], int]:
        """A friendly method to download a RedGifs media."""

        yarl_url = yarl.URL(url)
        str_url = str(yarl_url)

        def dl(url: str) -> int:
            r = self.__session.get(url, headers = self.headers)
            _log.debug(f'GET {url} returned code: {r.status_code}')

            if r.status_code == 404:
                raise HTTPException(r, r.json())

            content_type = r.headers['Content-Type']
            if content_type not in ['video/mp4', 'image/jpeg']:
                _log.error(f'GET {url} returned improper content-type: {content_type}')
                raise TypeError(f'"{url}" returned invalid content type for downloading: {content_type}')

            data = r.content
            if isinstance(fp, io.BufferedIOBase):
                return fp.write(data)
            else:
                with open(fp, 'wb') as f:
                    return f.write(data)

        if (yarl_url.host is not None and 'redgifs.com' in yarl_url.host):
            if 'watch' in yarl_url.path:
                id = yarl_url.path.strip('/watch/')
                hd_url = self.get_gif(id)['gif']['urls'].get('hd') or self.get_gif(id)['gif']['urls'].get('sd')
                return dl(hd_url)
            else:
                return dl(str_url)

        raise TypeError(f'"{strip_ip(str_url)}" is not a valid RedGifs URL')


class AsyncHttp:
    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        *,
        proxy: Optional[str] = None,
        proxy_auth: Optional[ProxyAuth] = None
    ) -> None:

        if session is not None and session is not isinstance(session, aiohttp.ClientSession):
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

    async def close(self) -> None:
        await self.__session.close()

    async def get_temp_token(self):
        return (await self.request(Route('GET', '/v2/auth/temporary')))

    # TODO: Implement OAuth login support
    async def login(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        if (username and password) is None:
            temp_token = await self.get_temp_token()
            self.headers['authorization'] = f'Bearer {temp_token["token"]}'
        else:
            raise NotImplementedError
    
    # GIF methods

    def get_tags(self, **params: Any) -> Response[TagsResponse]:
        return self.request(Route('GET', '/v1/tags'), **params)

    def get_gif(self, id: str, **params: Any) -> Response[GetGifResponse]:
        return self.request(Route('GET', '/v2/gifs/{id}', id=id), **params)

    def search(self, search_text: str, order: Order, count: int, page: int, **params: Any) -> Response[GifResponse]:
        r = Route(
            'GET', '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)

    def get_top_this_week(self, count: int, page: int, type: MediaType, **params) -> Response[GifResponse]:
        r = Route(
            'GET', '/v2/gifs/search?order=top7&count={count}&page={page}&type={type}',
            count=count, page=page, type=type.value
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
    ) -> Response[CreatorsResponse]:
        url = '/v1/creators/search?page={page}&order={order}'
        if verified:
            url += '&verified={verified}'
        if tags:
            url += '&tags={tags}'
            r = Route(
                'GET', url,
                page=page, order=order.value, verified='y' if verified else 'n', tags=','.join(t for t in tags)
            )
            return self.request(r, **params)
        else:
            r = Route(
                'GET', url,
                page=page, order=order.value, verified='y' if verified else 'n'
            )
            return self.request(r, **params)

    def search_creator(self, username: str, page: int, count: int, order: Order, type: MediaType, **params) -> Response[CreatorResponse]:
        r = Route(
            'GET', '/v2/users/{username}/search?page={page}&count={count}&order={order}&type={type}',
            username=username, page=page, count=count, order=order.value, type=type.value
        )
        return self.request(r, **params)

    def get_trending_gifs(self) -> Response[GifResponse]:
        r = Route('GET', '/v2/explore/trending-gifs')
        return self.request(r)

    # Pic methods

    def search_image(self, search_text: str, order: Order, count: int, page: int, **params: Any) -> Response[ImageResponse]:
        r = Route(
            'GET', '/v2/gifs/search?search_text={search_text}&order={order}&count={count}&page={page}&type=i',
            search_text=search_text, order=order.value, count=count, page=page
        )
        return self.request(r, **params)

    def get_trending_images(self) -> Response[TrendingImagesResponse]:
        r = Route('GET', '/v2/explore/trending-images')
        return self.request(r)

    # Tag methods

    def get_trending_tags(self) -> Response[TagsResponse]:
        r = Route('GET', '/v2/search/trending')
        return self.request(r)

    def get_tag_suggestions(self, query: str) -> Response[List[TagSuggestion]]:
        r = Route('GET', '/v2/search/suggest?query={query}', query=query)
        return self.request(r)

    # download

    async def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]) -> int:
        yarl_url = yarl.URL(url)
        str_url = str(yarl_url)

        async def dl(url: str) -> int:
            async with self.__session.get(url, headers = self.headers) as r:
                _log.debug(f'GET {str_url} returned code: {r.status}')

                content_type = r.headers['Content-Type']
                if content_type not in ['video/mp4', 'image/jpeg']:
                    _log.error(f'GET {url} returned improper content-type: {content_type}')
                    raise TypeError(f'"{url}" returned invalid content type for downloading: {content_type}')

                data = await r.read()
                if isinstance(fp, io.BufferedIOBase):
                    return (fp.write(data))
                else:
                    with open(fp, 'wb') as f:
                        return f.write(data)

        if (yarl_url.host is not None and 'redgifs.com' in yarl_url.host):
            if 'watch' in yarl_url.path:
                id = yarl_url.path.strip('/watch/')
                hd_url = (await self.get_gif(id))['gif']['urls'].get('hd') or (await self.get_gif(id))['gif']['urls'].get('sd')
                return (await dl(hd_url))
            else:
                return (await dl(str_url))

        raise TypeError(f'"{strip_ip(str_url)}" is not a valid RedGifs URL')
