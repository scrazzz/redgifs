from typing import List, Optional, TypedDict

from .gif import MediaInfo
from .niches import NichesInfo
from .user import UserInfo


class ImageInfo(TypedDict):
    id: str
    client_id: Optional[str]
    createDate: int
    # hasAudio: bool
    width: int
    height: int
    likes: int
    tags: List[str]
    verified: bool
    views: Optional[int]
    published: bool
    type: int # Literal[1,2]
    urls: MediaInfo
    userName: str
    avgColor: str
    # gallery: str
    niches: List[str]
    sexuality: Optional[List[str]]


# NOTE: even though this is an image, the field for this is `gifs`
# NOTE: see the type of `gifs` key.
class CommonImageResponse(TypedDict):
    page: int
    pages: int
    total: int
    gifs: List[ImageInfo]
    users: List[UserInfo]
    niches: List[NichesInfo]
    tags: List[str]


class TrendingImagesResponse(CommonImageResponse):
    pass


class ImageResponse(CommonImageResponse):
    pass
