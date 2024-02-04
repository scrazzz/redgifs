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
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

import aiohttp

from .http import AsyncHttp, ProxyAuth
from .tags import Tags
from .enums import Order, Type
from .utils import _async_read_tags_json, build_file_url, _gifs_iter, _images_iter, to_web_url
from .parser import parse_feeds, parse_search, parse_creator, parse_creators, parse_search_image
from .models import GIF, URL, CreatorResult, Feeds, Image, SearchResult, CreatorsResult

if TYPE_CHECKING:
    from redgifs.types.tags import TagInfo

class API:
    """The API Instance to get information from the RedGifs API.

    Parameters
    ----------
    session: Optional[:class:`aiohttp.ClientSession`]
        An :class:`aiohttp.ClientSession` object that can be provided to do the requests.
        If not provided, a new session object is created.
    proxy: Optional[:class:`str`]
        A valid proxy URL.
    proxy_auth: Optional[:class:`redgifs.ProxyAuth`]
        The proxy auth to provide if the proxy requires it.
    """
    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        *,
        proxy: Optional[str] = None,
        proxy_auth: Optional[ProxyAuth] = None,
    ) -> None:
        self.http: AsyncHttp = AsyncHttp(session, proxy=proxy, proxy_auth=proxy_auth)
        self._tags = Tags()

    async def login(self) -> 'API':
        """
        A method to login to RedGifs with a temporary token.
        You must use this method after initialising the :py:class:`API <redgifs.aio.API>` class 
        for this library to function properly.

        Returns
        -------
        :py:class:`API <redgifs.aio.API>`
            The properly initialised API class.
        """
        await self.http.login()
        return self

    async def get_feeds(self) -> Feeds:
        """Get RedGifs homepage feeds.
        
        Returns
        -------
        :py:class:`Feeds <redgifs.models.Feeds>` - The Feed info.
        """
        feeds = await self.http.get_feeds()
        return parse_feeds(feeds)

    async def get_tags(self) -> List[TagInfo]:
        """Get all available RedGifs Tags.
        
        Returns
        -------
        ``List[Dict[str, Union[str, int]]]``
        """
        resp = await self.http.get_tags()
        return resp['tags']

    async def get_gif(self, id: str) -> GIF:
        """
        Get details of a single GIF uisng its ID.

        Parameters
        ----------
        id: :class:`str`
            The ID of the GIF.

        Returns
        -------
        :py:class:`GIF <redgifs.models.GIF>` - The GIF's info.
        """
        json = (await self.http.get_gif(id))['gif']
        urls = json['urls']
        return GIF(
            id=json['id'],
            create_date=datetime.utcfromtimestamp(json['createDate']),
            has_audio=json['hasAudio'],
            width=json['width'],
            height=json['height'],
            likes=json['likes'],
            tags=json['tags'],
            verified=json['verified'],
            views=json.get('views'),
            duration=json['duration'],
            published=json['published'],
            urls=URL(
                sd=urls['sd'],
                hd=urls['hd'],
                poster=urls['poster'],
                thumbnail=urls['thumbnail'],
                vthumbnail=urls.get('vthumbnail'),
                web_url=to_web_url(json['id']),
                file_url=build_file_url(urls['sd'])
            ),
            username=json['userName'],
            type=json['type'],
            avg_color=json['avgColor'],
        )

    async def get_trending_gifs(self) -> List[GIF]:
        """
        Get the top 10 trending GIFs on RedGifs.

        Returns
        -------
        List[:py:class:`Image <redgifs.models.Image>`]
        """
        r = (await self.http.get_trending_gifs())['gifs']
        return _gifs_iter(r)

    async def get_trending_images(self) -> List[Image]:
        """
        Get the top 10 trending images on RedGifs.

        Returns
        -------
        List[:py:class:`Image <redgifs.models.Image>`]
        """
        r = (await self.http.get_trending_images())['gifs']
        return _images_iter(r)

    async def get_trending_tags(self) -> List[TagInfo]:
        """Get the trending searches on RedGifs.

        Returns
        -------
        ``List[Dict[str, Union[str, int]]]``
            A list of dicts containing the tag name and count::

                [
                    {
                        "name": "r/CaughtPublic",
                        "count": 2034
                    },
                    {
                        "name": "Vintage",
                        "count": 19051
                    },
                    ...
                ]
        """
        result = (await self.http.get_trending_tags())['tags']
        return result

    async def get_top_this_week(self, count: int = 30, page: int = 1, type: Type = Type.gif) -> SearchResult:
        """Get media from "Top This Week" section.

        Parameters
        ----------
        count: :class:`int`
            The number of items to return.
        page: :class:`int`
            The items to return from given page number.
        type: :class:`Order`
            The type of media to return.

        Returns
        -------
        :class:`SearchResult <redgifs.models.SearchResult>` - Top this week results.
        """
        resp = await self.http.get_top_this_week(count, page, type)
        return parse_search('TopThisWeek', resp)

    async def fetch_tag_suggestions(self, query: str) -> List[str]:
        """Get tag suggestions from RedGifs.

        .. note::

            It's advised to use :func:`Tags.search() <redgifs.Tags.search()>` to prevent multiple API calls to redgifs.com.

        Parameters
        ----------
        query: :class:`str`
            The tag name to look for.

        Returns
        -------
        ``List[str]``
            A list of tag names.
        """
        result = await self.http.get_tag_suggestions(query)
        return [d['text'] for d in result] # type: ignore - `get_tag_suggestions` isn't properly TypedDict'd so ignore the warning

    async def search(
        self,
        search_text: str,
        *,
        order: Order = Order.trending,
        count: int = 80,
        page: int = 1,
    ) -> SearchResult:
        """
        Search for GIFs.

        Parameters
        ----------
        search_text: :class:`str`
            The type of GIFs to search for. Can be a string or an instance of :class:`Tags`.
        order: Optional[:class:`Order`]
            The order of the GIFs to return.
        count: Optional[:class:`int`]
            The amount of GIFs to return.
        page: Optional[:class:`int`]
            The page number of the GIFs to return.

        Returns
        -------
        :py:class:`SearchResult <redgifs.models.SearchResult>` - The search result.
        """
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
        tags: Optional[List[str]] = None,
    ) -> CreatorsResult:
        """
        Search for some RedGifs Creators.

        Parameters
        ----------
        page: Optional[:class:`int`]
            The result in page number to return.
        order: Optional[:class:`Order <redgifs.Order>`]
            The order of the creators to return.
        verified: Optional[:class:`bool`]
            Wheather to only return verified creators.
        tags: Optional[List[:class:`str`]]
            A list of tags to look for.
            Narrows down the results to creators that have contents with the given tags.

        Returns
        -------
        :py:class:`CreatorsResult <redgifs.models.CreatorsResult>` - The search result.
        """
        resp = await self.http.search_creators(page=page, order=order, verified=verified, tags=tags)
        return parse_creators(resp)

    async def search_creator(
        self,
        username: str,
        *,
        page: int = 1,
        count: int = 80,
        order: Order = Order.recent,
        type: Type = Type.gif,
    ) -> CreatorResult:
        """
        Search for a single RedGifs creator/user by username.

        Parameters
        ----------
        username: :class:`str`
            The username of the creator/user.
        page: :class:`int`
            The current page number of the creator/user's profile.
        count: :class:`int`
            The total amount of GIFs to return.
        order: :class:`Order`
            The order to return creator/user's GIFs.

        Returns
        -------
        :py:class:`CreatorResult <redgifs.models.CreatorResult>` - The creator/user searched for.
        """
        resp = await self.http.search_creator(username=username, page=page, count=count, order=order, type=type)
        return parse_creator(resp, type)

    search_user = search_creator

    async def search_image(
        self,
        search_text: str,
        *,
        order: Order = Order.new,
        count: int = 80,
        page: int = 1,
    ) -> SearchResult:
        """
        Search for images.

        Parameters
        ----------
        search_text: :class:`str`
            The images to search for. Can be a string or an instance of :class:`Tags <redgifs.Tags>`.
        order: Optional[:class:`Order`]
            The order of the images to return.
        count: Optional[:class:`int`]
            The amount of images to return.
        page: Optional[:class:`int`]
            The page number of the images to return.

        Returns
        -------
        :py:class:`SearchResult <redgifs.models.SearchResult>` - The search result.
        """
        # We are not going to use Tags.search() here because it doesn't matter
        # whatever the search_text is, this API endpoints provides images nonetheless.
        resp = await self.http.search_image(search_text, order, count, page)
        return parse_search_image(search_text, resp)

    async def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]) -> int:
        """
        A friendly method to download a RedGifs media.

        Example:

        .. code-block:: python

            from redgifs.aio import API

            api = API()
            await api.login()
            hd_url = await api.search("query").gifs[0].urls.hd
            await api.download(hd_url, "video.mp4")

        .. note::
            
            You should use this method to download any media from RedGifs
            because RedGifs does validation on User-Agents and other params. 
            If you try to download it by using any other means, it will return a 403 error.

        Parameters
        ----------
        url: str
            A valid RedGifs URL.
        fp: Union[:class:`io.BufferedIOBase`, :class:`os.PathLike`]
            The file-like object to save this asset to or the filename
            to use. If a filename is passed then a file is created with that
            filename and used instead.
        """
        return (await self.http.download(url, fp))

    async def close(self) -> None:
        """Closes the API session."""
        return (await self.http.close())
