from typing import List, TypedDict

from .user import UserInfo
from .gif import GifInfo
from .image import ImageInfo


class FeedsResponse(TypedDict):
    horizontalGifs: List[GifInfo]
    hotCreators: List[UserInfo]
    hotGifs: List[GifInfo]
    hotImages: List[ImageInfo]
    longGifs: List[GifInfo]
    newCreators: List[UserInfo]
    soundGifs: List[GifInfo]
    verifiedGifs: List[GifInfo]
    verifiedImages: List[ImageInfo]
    verticalGifs: List[GifInfo]
