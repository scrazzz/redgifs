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
from typing import Dict, List, Optional

@dataclass
class URL:
    """The different types of URLs.

    .. warning::

        ``sd``, ``hd``, ``poster``, ``thumbnail``, and ``vthumbnail`` leaks your IP address in the URL.
        If you want to display the URLs to the end user consider using ``web_url`` or ``file_url`` instead.

    Attributes
    ----------
    sd: :class:`str`
        The sd URL of the GIF.
    hd: :class:`str`
        The hd URL of the GIF.
    poster: :class:`str`
        The poster URL of the GIF.
    thumbnail: :class:`str`
        The thumbnail URL of the GIF.
    vthumbnail: :class:`str`
        The vthumbnail URL of the GIF.
    web_url: :class:`str`
        The website URL of the GIF.
    file_url: Optional[:class:`str`]
        The file URL of the GIF.
    """

    __slots__ = ('sd', 'hd', 'poster', 'thumbnail', 'vthumbnail', 'web_url', 'file_url')

    sd: str
    hd: str
    poster: str
    thumbnail: str
    vthumbnail: str
    web_url: str
    file_url: Optional[str]

@dataclass
class GIF:
    # TODO: Document "type" and "avg_color"
    """The GIF returned from RedGifs.

    Attributes
    ----------
    id: :class:`str`
        The GIF's ID.
    create_date: Optional[:class:`datetime.datetime`]
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

    id: str
    create_date: Optional[datetime.datetime]
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
class Image:
    # TODO: Document "type" and "avg_color"
    """The image returned from RedGifs.

    Attributes
    ----------
    id: :class:`str`
        The image ID.
    create_date: Optional[:class:`datetime.datetime`]
        The date when the image is published.
    width: :class:`int`
        The image width.
    height: :class:`int`
        The image height.
    likes: :class:`int`
        The amount of likes the image has.
    tags: List[:class:`str`]
        A list of tags for the GIF.
    verified: :class:`bool`
        Wheather the publisher of the image is a verified creator.
    views: :class:`int`
        The amount of views the image has.
    published: :class:`bool`
        Wheather the image is published.
    urls: :class:`URL`
        The different types of URLs for the image.
    username: :class:`str`
        The username of the publisher.
    type: :class:`int`

    avg_color: :class:`str`

    """

    __slots__ = (
        'id', 'create_date', 'width', 'height',
        'likes', 'tags', 'verified', 'views',
        'published', 'urls', 'username', 'type', 'avg_color',
    )

    id: str
    create_date: Optional[datetime.datetime]
    width: int
    height: int
    likes: int
    tags: List[str]
    verified: bool
    views: int
    published: bool
    urls: URL
    username: str
    type: int
    avg_color: str

@dataclass
class User:
    # TODO: Document "subscription"
    """The user's information returned from RedGifs.

    Attributes
    ----------
    creation_time: Optional[:class:`datetime.datetime`]
        The user's account creation time.
    description: Optional[:class:`str`]
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
        The user's "profile URL".
        This is NOT the user's URL on ``redgifs.com``, see :py:attr:`url <redgifs.models.User.url>` for that.
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
        The user's total amount of views of all the GIFs published.
    poster: Optional[:class:`str`]
        The user's poster URL.
    preview: Optional[:class:`str`]
        The user's preview URL.
    thumbnail: Optional[:class:`str`]
        The user's thumbnail URL.
    links: Optional[List[Dict[:class:`str`, :class:`str`]]]
        The linked websites on the user's profile.
    """

    __slots__ = (
        'creation_time', 'description', 'followers', 'following', 'gifs',
        'name', 'profile_image_url', 'profile_url', 'published_collections', 'published_gifs',
        'status', 'subscription', 'url', 'username', 'verified',
        'views', 'poster', 'preview', 'thumbnail', 'links'
    )

    creation_time: Optional[datetime.datetime]
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
    links: Optional[List[Dict[str, str]]]

@dataclass
class SearchResult:
    # TODO: Document "users"
    """The result you have searched. This is returned in :py:meth:`API.search() <redgifs.API.search()>`.

    Attributes
    ----------
    searched_for: :class:`str`
        The result of what you have searched for.
        This may differ from what you have provided for ``query`` in :py:meth:`API.search() <redgifs.API.search()>`.
    page: :class:`int`
        The current page number.
    pages: :class:`int`
        The total number of pages for the query.
    total: :class:`int`
        The total number of GIFs for the query.
    gifs: Optional[List[:class:`GIF`]]
        The GIFs which was searched for.
    images: Optional[List[:class:`Image`]]
        The images which was searched for.
    users: List[:class:`User`]

    tags: List[:class:`str`]
        The tags related to the GIFs and search query.
    """

    __slots__ = (
        'searched_for', 'page', 'pages', 'total', 'gifs', 'images', 'users', 'tags',
    )

    searched_for: str
    page: int
    pages: int
    total: int
    gifs: Optional[List[GIF]]
    images: Optional[List[Image]]
    users: List[User]
    tags: List[str]

@dataclass
class CreatorsResult:
    # TODO: Document "total"
    """The creator results searched for.

    Attributes
    ----------
    items: List[:class:`User`]
        The list of creators.
    page: :class:`int`
        The current page number.
    pages: :class:`int`
        The total number of pages available.
    total: :class:`int`

    """

    __slots__ = ('items', 'page', 'pages', 'total')

    items: List[User]
    page: int
    pages: int
    total: int

@dataclass
class CreatorResult:
    """The creator result searched for.

    Attributes
    ----------
    creator: :class:`User`
        The creator/user details.
    page: :class:`int`
        The current page number.
    pages: :class:`int`
        The total number of pages available.
    total: :class:`int`
        The total number of GIFs this creator/user has created.
    """

    __slots__ = ('creator', 'page', 'pages', 'total', 'gifs')

    creator: User
    page: int
    pages: int
    total: int
    gifs: List[GIF]

@dataclass
class Feeds:
    """The RedGifs home feeds.

    Attributes
    ----------
    horizontal_gifs: List[:class:`GIF`]
    vertical_gifs: List[:class:`GIF`]
    hot_creators: List[:class:`User`]
    new_creators: List[:class:`User`]
    hot_gifs: List[:class:`GIF`]
    long_gifs: List[:class:`GIF`]
    verified_gifs: List[:class:`GIF`]
    sound_gifs: List[:class:`GIF`]
    hot_images: List[:class:`Image`]
    verified_images: List[:class:`Image`]
    """

    __slots__ = (
        'horizontal_gifs', 'vertical_gifs',
        'hot_creators', 'new_creators',
        'hot_gifs', 'long_gifs', 'verified_gifs', 'sound_gifs',
        'hot_images', 'verified_images'
    )

    horizontal_gifs: List[GIF]
    vertical_gifs: List[GIF]
    hot_creators: List[User]
    new_creators: List[User]
    hot_gifs: List[GIF]
    long_gifs: List[GIF]
    verified_gifs: List[GIF]
    sound_gifs: List[GIF]
    hot_images: List[Image]
    verified_images: List[Image]
