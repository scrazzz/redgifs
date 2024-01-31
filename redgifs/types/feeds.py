from typing import List, TypedDict
from redgifs.types.gif import GifInfo
from redgifs.types.image import ImageInfo

class FeedsResponse(TypedDict):
    horizontalGifs: List[GifInfo]
    hotCreators: List[GifInfo]
    hotGifs: List[GifInfo]
    hotImages: List[ImageInfo]
    longGifs: List[GifInfo]
    newCreators: List[ImageInfo]
    soundGifs: List[GifInfo]
    verifiedGifs: List[GifInfo]
    verifiedImages: List[ImageInfo]
    verticalGifs: List[GifInfo]
