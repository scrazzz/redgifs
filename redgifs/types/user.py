from typing import List, Optional, TypedDict, Union

from .image import ImageInfo
from .gif import GifInfo
from .niches import NichesInfo


class UserInfo(TypedDict):
    creationtime: int
    description: Optional[str]
    followers: int
    following: int
    gifs: int
    name: str
    profileImageUrl: Optional[str]
    profileUrl: str
    publishedCollections: Optional[int]
    publishedGifs: int
    status: Optional[str]
    subscription: int
    url: str
    username: str
    verified: bool
    views: int
    poster: Optional[str]
    preview: Optional[str]
    thumbnail: Optional[str]
    likes: Optional[int]


class CreatorInfo(UserInfo):
    pass


# NOTE: See type of `gifs` field
class CreatorResponse(TypedDict):
    page: int
    pages: int
    total: int
    gifs: Union[List[GifInfo], List[ImageInfo]]
    users: List[UserInfo]
    niches: List[NichesInfo]
    tags: List[str]


class CreatorsResponse(TypedDict):
    page: int
    pages: int
    total: int
    items: List[UserInfo]
