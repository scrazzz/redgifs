from typing import List, TypedDict
from redgifs.types.gif import GifInfo, UserInfo

class GifResponse(TypedDict):
    gif: GifInfo

class SearchResponse(TypedDict):
    page: int
    pages: int
    total: int
    gifs: List[GifInfo]
    users: List[UserInfo]
    tags: List[str]
