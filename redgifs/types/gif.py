from typing import List, Optional, TypedDict

from .niches import NichesInfo
from .user import UserInfo

class MediaInfo(TypedDict):
    sd: str
    hd: str
    gif: str
    poster: str
    thumbnail: str
    vthumbnail: Optional[str]


class GifInfo(TypedDict):
    id: str
    client_id: Optional[str]
    createDate: int
    hasAudio: bool
    width: int
    height: int
    likes: int
    tags: List[str]
    verified: bool
    views: Optional[int]
    duration: float
    published: bool
    type: int # Literal[1,2]
    urls: MediaInfo
    userName: str
    avgColor: str
    gallery: str


class GetGifResponse(TypedDict):
    gif: GifInfo
    user: Optional[UserInfo]


class CommonGifResponse(TypedDict):
    page: int
    pages: int
    total: int
    gifs: List[GifInfo]
    users: List[UserInfo]
    niches: List[NichesInfo]
    tags: List[str]


class GifResponse(CommonGifResponse):
    pass
