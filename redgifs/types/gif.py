from typing import List, Optional, TypedDict

class UserInfo(TypedDict):
    creationtime: int
    description: str
    followers: int
    following: int
    gifs: int
    name: str
    profileImageUrl: str
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

class MediaInfo(TypedDict):
    sd: str
    hd: str
    gif: str
    poster: str
    thumbnail: str
    vthumbnail: str

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
    gallry: str
