from typing import TypedDict, List


class BaseNicheInfo(TypedDict):
    gifs: int
    id: str
    name: str
    subscribers: int
    thumbnail: str

class NichesInfo(BaseNicheInfo):
    cover: str
    description: str
    owner: str
    rules: str

class NicheBriefInfo(BaseNicheInfo):
    tags: List[str]
    preferences: List[str]

class NicheResponse(TypedDict):
    page: int
    pages: int
    total: int
    niches: List[NicheBriefInfo]