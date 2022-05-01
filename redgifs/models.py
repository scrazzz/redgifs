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

import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class URL:
    """The different types of URLs.

    Attributes
    ----------
    sd: :class:`str`

    hd: :class:`str`

    poster: :class:`str`

    thumbnail: :class:`str`

    vthumbnail: :class:`str`

    """

    __slots__ = ('sd', 'hd', 'poster', 'thumbnail', 'vthumbnail')

    sd: str
    hd: str
    poster: str
    thumbnail: str
    vthumbnail: str

@dataclass
class Gif:
    # TODO: Document "type" and "avg_color"
    """The GIF returned from RedGifs.

    Attributes
    ----------
    id: :class:`str`
        The GIF's ID.
    create_date: :class:`datetime.datetime`
        The date when the GIF is published.
    has_audio: :class:`bool`
        Wheather the GIF has sound.
    width: :class:`int`
        The GIF's width.
    height: :class:`int`
        The GIF's height.
    likes: :class:`int`
        The amount of likes for the GIF.
    tags: List[:class:`str`]
        A list of tags for the GIF.
    verified: :class:`bool`
        Wheather the publisher of the GIF is a verified creator.
    views: :class:`int`
        The amount of views for the GIF.
    duration: :class:`int`
        The GIF's duration in seconds.
    published: :class:`bool`
        Wheather the GIF is published.
    urls: :class:`URL`
        The different types of URLs for the GIF.
    username: :class:`str`
        The username of the publisher.
    type: :class:`int`

    avg_color: :class:`str`

    """

    __slots__ = (
        'id', 'create_date', 'has_audio', 'width', 'height',
        'likes', 'tags', 'verified', 'views', 'duration',
        'published', 'urls', 'username', 'type', 'avg_color',
    )

    id: int
    create_date: datetime.datetime
    has_audio: bool
    width: int
    height: int
    likes: int
    tags: List[str]
    verified: bool
    views: int
    duration: int
    published: bool
    urls: URL
    username: str
    type: int
    avg_color: str
    # gallery

@dataclass
class User:
    # TODO: Document "subscription"
    """The user's information returned from RedGifs.

    Attributes
    ----------
    creation_time: :class:`datetime.datetime`
        The user's account creation time.
    description: :class:`str`
        The user's description on their profile.
    followers: :class:`int`
        The user's amount of followers.
    following: :class:`int`
        The user's amount of following users.
    gifs: :class:`int`
        The user's total amount of GIFs published.
    name: Optional[:class:`str`]
        The user's name.
    profile_image_url: Optional[:class:`str`]
        The user's profile image URL.
    profile_url: :class:`str`
        The user's profile URL.
        This is not the user's URL on ``redgifs.com``.
    published_collections: :class:`int`
        The user's amount of published collections.
    published_gifs: :class:`int`
        The user's amount of published GIFs.
    status: :class:`str`
        The user's status.
    subscription: :class:`int`

    url: :class:`str`
        The user's URL on ``redgifs.com``.
    username: :class:`str`
        The user's username.
    verified: :class:`bool`
        Wheather the user is a verified creator.
    views: :class:`int`
        The user's total amount of views of the GIFs published.
    poster: Optional[:class:`str`]
        The user's poster.
    preview: Optional[:class:`str`]
        The user's preview.
    thumbnail: Optional[:class:`str`]
        The user's thumbnail.
    """

    __slots__ = (
        'creation_time', 'description', 'followers', 'following', 'gifs',
        'name', 'profile_image_url', 'profile_url', 'published_collections', 'published_gifs',
        'status', 'subscription', 'url', 'username', 'verified',
        'views', 'poster', 'preview', 'thumbnail',
    )

    creation_time: datetime.datetime
    description: Optional[str]
    followers: int
    following: int
    gifs: int
    name: str
    profile_image_url: str
    profile_url: str
    published_collections: int
    published_gifs: int
    status: str
    subscription: int
    url: str
    username: str
    verified: bool
    views: int
    poster: Optional[str]
    preview: Optional[str]
    thumbnail: Optional[str]

@dataclass
class SearchResult:
    # TODO: Document "users"
    """The result you have searched. This is returned in :py:meth:`search() <redgifs.API.search()>`.

    Attributes
    ----------
    searched_for: :class:`str`
        The result of what you have searched for.
        This may differ from what you have provided for ``query`` in :py:meth:`search <redgifs.API.search()>`.
    page: :class:`int`
        The current page number.
    pages: :class:`int`
        The total number of pages for the query.
    total: :class:`int`
        The total number of GIFs for the query.
    gifs: List[:class:`Gif`]
        The GIFs which was searched for.
    users: List[:class:`User`]

    tags: List[:class:`str`]
        The tags related to the GIFs and search query.
    """

    __slots__ = (
        'searched_for', 'page', 'pages', 'total', 'gifs', 'users', 'tags',
    )

    searched_for: str
    page: int
    pages: int
    total: int
    gifs: List[Gif]
    users: List[User]
    tags: List[str]

@dataclass
class CreatorsResult:
    # TODO: Document "total"
    """The creator result you have searched.

    Attributes
    ----------
    items: List[:class:`User`]
        The list of creators.
    pages: :class:`int`
        The total number of pages.
    page: :class:`int`
        The current page number.
    total: :class:`int`

    """

    __slots__ = (
        'items', 'pages', 'page', 'total'
    )

    items: List[User]
    pages: int
    page: int
    total: int
