from typing import List, TypedDict


class TagInfo(TypedDict):
    name: str
    count: int


class TagsResponse(TypedDict):
    tags: List[TagInfo]


class TagSuggestion(TypedDict):
    gifs: int
    text: str
    type: str
