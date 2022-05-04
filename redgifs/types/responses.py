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

from typing import Dict, List, Optional, TypedDict, Union

class URL(TypedDict):
    sd: str
    hd: str
    poster: str
    thumbnail: str
    vthumbnail: str

class GIF(TypedDict):
    id: int
    createDate: int
    hasAudio: bool
    width: int
    height: int
    likes: int
    tags: List[str]
    verified: bool
    views: int
    duration: int
    published: bool
    urls: URL
    userName: str
    type: int
    avgColor: str
    # gallery: None

class User(TypedDict):
    creationtime: int
    description: Optional[str]
    followers: int
    following: int
    gifs: int
    name: str
    profileImageUrl: str
    profileUrl: str
    publishedCollections: int
    publishedGifs: int
    status: str
    subscription: int
    url: str
    username: str
    verified: bool
    views: int
    poster: Optional[str]
    preview: Optional[str]
    thumbnail: Optional[str]


class TagsResult(TypedDict):
    tags: List[Dict[str, Union[str, int]]]

class SearchResult(TypedDict):
    page: int
    pages: int
    total: int
    gifs: List[GIF]
    tags: List[str]

class CreatorsResult(TypedDict):
    items: List[User]
    pages: int
    page: int
    total: int
