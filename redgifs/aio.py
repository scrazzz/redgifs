"""
The MIT License (MIT)

Copyright (c) 2022-present scrazzz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from typing import List, Optional, Union

from .http import *
from .enums import Tags

class API:
    def __init__(self) -> None:
        self.http = AsyncHttp()

    async def get_tags(self):
        return (await self.http.get_tags())

    async def search(self, search_text: Union[str, Tags], *, order: Order = Order.recent, count: int = 80, page: int = 1):
        if isinstance(search_text, str):
            query = Tags.search(search_text)
        elif isinstance(search_text, Tags):
            query = search_text
        return (await self.http.search(query, order, count, page))
    
    async def search_creators(self, *, page: int = 1, order: Order = Order.recent, verified: bool = False, tags: Optional[Union[List[Tags], List[str]]] = None):
        resp = await self.http.search_creators(page=page, order=order, verified=verified, tags=tags)
        return resp

    async def get_gif(self, id: str):
        resp = await self.http.get_gif(id)
        return resp

    async def close(self) -> None:
        return (await self.http.close())
