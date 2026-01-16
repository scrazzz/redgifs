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
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, List, Optional, Union

import requests

from .tags import Tags
from .enums import Order, MediaType
from .http import HTTP, ProxyAuth
from .utils import _read_tags_json, build_file_url, _gifs_iter, _images_iter, to_embed_url, to_web_url
from .parser import parse_creator, parse_search, parse_creators, parse_search_image
from .models import URL, GIF, CreatorResult, Image, SearchResult, CreatorsResult, TagSuggestion, User

if TYPE_CHECKING:
    from redgifs.types.tags import TagInfo

__all__ = ('API',)


class API:
    """The API Instance to get information from the RedGifs API.

    .. note::

        If you are using this library in an asynchronous code,
        you should refer the :ref:`Async API` section.

    Parameters
    ----------
    session: Optional[:class:`requests.Session`]
        A session object that can be provided to do the requests.
        If not provided, a new session object is created.
    proxy: Optional[:class:`str`]
        A valid proxy URL.
    proxy_auth: Optional[:class:`.ProxyAuth`]
        The proxy auth to provide if the proxy requires it.
    """

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        *,
        proxy: Optional[str] = None,
        proxy_auth: Optional[ProxyAuth] = None,
    ) -> None:
        self.http: HTTP = HTTP(session, proxy=proxy, proxy_auth=proxy_auth)
        self._tags = Tags()

    def login(self) -> 'API':
        """
        A method to login to RedGifs with a temporary token.
        You must use this method after initialising the :class:`API <redgifs.API>` class
        for this library to function properly.

        Returns
        -------
        :class:`API` - The properly initialised API class.
        """
        self.http.login()
        return self

    def get_tags(self) -> List[TagInfo]:
        """Get all available RedGifs Tags.

        Returns
        -------
        ``List[Dict[str, Union[str, int]]]``
        """
        return self.http.get_tags()['tags']

    def get_gif(self, id: str) -> GIF:
        """
        Get details of a single GIF using its ID.

        If the URL is ``https://redgifs.com/watch/abcxyz`` then the ID is ``abcxyz``.

        Parameters
        ----------
        id: :class:`str`
            The ID of the GIF.

        Returns
        -------
        :class:`.GIF` - The GIF's info.
        """

        json = self.http.get_gif(id)['gif']
        urls = json['urls']
        return GIF(
            id=json['id'],
            create_date=datetime.fromtimestamp(json['createDate'], tz=timezone.utc),
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
                hd=urls.get('hd'),
                poster=urls.get('poster'),
                thumbnail=urls['thumbnail'],
                vthumbnail=urls.get('vthumbnail'),
                web_url=to_web_url(json['id']),
                file_url=build_file_url(urls['sd']),
                embed_url=to_embed_url(urls['sd']),
            ),
            username=json['userName'],
            type=json['type'],
            avg_color=json['avgColor'],
        )

    def get_trending_gifs(self) -> List[GIF]:
        """
        Get the top 10 trending GIFs on RedGifs.

        Returns
        -------
        List[:class:`.GIF`]
        """
        r = self.http.get_trending_gifs()['gifs']
        return _gifs_iter(r)

    def get_trending_images(self) -> List[Image]:
        """
        Get the top 10 trending images on RedGifs.

        Returns
        -------
        List[:class:`.Image`]
        """
        r = self.http.get_trending_images()['gifs']
        return _images_iter(r)

    def get_trending_tags(self) -> List[TagInfo]:
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
        resp = self.http.get_trending_tags()['tags']
        return resp

    def get_top_this_week(self, count: int = 30, page: int = 1, type: MediaType = MediaType.GIF) -> SearchResult:
        """Get media from "Top This Week" section.

        Parameters
        ----------
        count: :class:`int`
            The number of items to return.
        page: :class:`int`
            The items to return from given page number.
        type: :class:`.MediaType`
            The type of media to return.

        Returns
        -------
        :class:`.SearchResult` - Top this week results.
        """
        resp = self.http.get_top_this_week(count, page, type)
        return parse_search('TopThisWeek', resp, type)

    def fetch_tag_suggestions(self, query: str) -> List[TagSuggestion]:
        """Get tag suggestions from RedGifs.

        .. note::

            It's advised to use :func:`Tags.search()` to prevent multiple API calls to redgifs.com.

        Parameters
        ----------
        query: :class:`str`
            The tag name to look for.

        Returns
        -------
        List[:class:`.TagSuggestion`] - A list of ``TagSuggestion`` with tag name and count.
        """
        result = self.http.get_tag_suggestions(query)
        return [TagSuggestion(name=d['text'], count=d['gifs']) for d in result]

    def search(self, search_text: str, *, order: Order = Order.TRENDING, count: int = 40, page: int = 1) -> SearchResult:
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
        :class:`.SearchResult` - The search result.
        """
        if len(self._tags.tags_mapping) == 0:
            tags = _read_tags_json()
            self._tags._set(tags)

        st = self._tags.search(search_text)[0]
        resp = self.http.search(st, order, count, page)
        return parse_search(st, resp, MediaType.GIF)

    search_gif = search

    def search_creators(
        self,
        *,
        page: int = 1,
        order: Order = Order.RECENT,
        verified: bool = False,
        tags: Optional[List[str]] = None,
    ) -> CreatorsResult:
        """
        Search for some RedGifs Creators.

        Parameters
        ----------
        page: Optional[:class:`int`]
            The result in page number to return.
        order: Optional[:class:`.Order`]
            The order of the creators to return.
        verified: Optional[:class:`bool`]
            Wheather to only return verified creators.
        tags: Optional[List[:class:`str`]]
            A list of tags to look for.
            Narrows down the results to creators that have contents with the given tags.

        Returns
        -------
        :class:`.CreatorsResult` - The search result.
        """
        resp = self.http.search_creators(page=page, order=order, verified=verified, tags=tags)
        return parse_creators(resp)

    def search_creator(
        self,
        username: str,
        *,
        page: int = 1,
        count: int = 80,
        order: Order = Order.RECENT,
        type: MediaType = MediaType.GIF,
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
        type: :class:`.MediaType`
            Whether to return image or GIF results. By default returns GIFs.

        Returns
        -------
        :class:`.CreatorResult` - The creator/user searched for.
        """
        resp = self.http.search_creator(username, page=page, count=count, order=order, type=type)
        return parse_creator(resp, type)

    search_user = search_creator

    def get_user(self, username: str):
        """
        Get details of a user on RedGifs.

        Parameters
        ----------
        username: :class:`str`
            The username of the user.

        Returns
        -------
        :class:`.User` - The user's details
        """
        resp = self.http.get_user(username)
        return User(
            creation_time=datetime.fromtimestamp(resp['creationtime'], tz=timezone.utc),
            description=resp.get('description'),
            followers=resp['followers'],
            following=resp['following'],
            gifs=resp['gifs'],
            name=resp.get('name'),
            links=resp.get('links'),
            poster=resp.get('poster'),
            preview=resp.get('preview'),
            profile_image_url=resp.get('profileImageUrl'),
            profile_url=resp.get('profileUrl'),
            published_collections=resp.get('publishedCollections'),
            published_gifs=resp['publishedGifs'],
            status=resp.get('status'),
            subscription=resp['subscription'],
            thumbnail=resp.get('thumbnail'),
            url=resp['url'],
            username=resp['username'],
            verified=resp['verified'],
            views=resp['views'],
        )

    def search_image(self, search_text: str, *, order: Order = Order.TRENDING, count: int = 40, page: int = 1) -> SearchResult:
        """
        Search for images.

        Parameters
        ----------
        search_text: :class:`str`
            The images to search for. Can be a string or an instance of :class:`Tags <redgifs.Tags>`.
        order: Optional[:class:`.Order`]
            The order of the images to return.
        count: Optional[:class:`int`]
            The amount of images to return.
        page: Optional[:class:`int`]
            The page number of the images to return.

        Returns
        -------
        :class:`.SearchResult` - The search result.
        """
        # We are not going to use Tags.search() here because it doesn't matter
        # whatever the search_text is, this API endpoints provides images nonetheless.
        resp = self.http.search_image(search_text, order, count, page)
        return parse_search_image(search_text, resp)

    def download(self, url: str, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase]):
        """
        A friendly method to download a RedGifs media.

        Example:

        .. code-block:: python

            api = redgifs.API()
            api.login()
            hd_url = api.search("query").gifs[0].urls.hd
            api.download(hd_url, "video.mp4")

        .. note::

            You should use this method to download any media from RedGifs
            because RedGifs does validation on User-Agents and other params.
            If you try to download it by using any other means, it will return 403 error.

        Parameters
        ----------
        url: :class:`str`
            A valid RedGifs URL.
        fp: Union[:class:`io.BufferedIOBase`, :class:`os.PathLike`]
            The file-like object to save this asset to or the filename
            to use. If a filename is passed then a file is created with that
            filename and used instead.
        """
        return self.http.download(url, fp)

    def close(self) -> None:
        """Closes the API session."""
        return self.http.close()
