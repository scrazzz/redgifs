from typing import Optional, TypedDict

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
