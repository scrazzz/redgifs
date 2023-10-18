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

import difflib
from random import choice, choices
from typing import Dict, List, Literal, overload

from .utils import _read_tags_json
from .errors import InvalidTag

class Tags:
    tags_mapping: Dict[str, str] = {}

    def _set(self, tags: Dict[str, str]) -> None:
        self.tags_mapping = tags

    def _clear(self) -> None:
        self.tags_mapping = {}

    def search(self, tag: str) -> List[str]:
        """
        Search for a specific RedGifs tag.

        .. note::

            This method is synchronous, a.k.a "blocking", when used alone.

        Parameters
        ----------
        tag: :class:`str`
            The tag name to search.

        Returns
        -------
        List[:class:`str`] - A list of tag names that are similar.
        """

        # If this method is being used alone, then `tags_mapping` needs to be set
        if len(self.tags_mapping) == 0:
            self._set(_read_tags_json())

        # Try to do a quick lookup, if it fails then go for difflib method
        try:
            return [self.tags_mapping[tag]]
        except KeyError:
            results = difflib.get_close_matches(tag.title(), self.tags_mapping.values())

            if len(results) == 0:
                raise InvalidTag(tag)

            return results

    @overload
    def random(self, count: Literal[1] = ...) -> str:
        ...
    
    @overload
    def random(self, count: int = ...) -> List[str]:
        ...

    def random(self, count: int = 1):
        """
        Search for random RedGifs tags.

        Parameters
        ----------
        count: :class:`int`
            The amount of tags to return.

        Returns
        -------
        Union[:class:`str`, List[:class:`str`]]
            If the ``count`` specified is ``1`` then a single random tag is returned
            or else a list of tags are returned.
        """
        return choices(list(self.tags_mapping.values()), k=count) if count != 1 \
        else choice(list(self.tags_mapping.values()))
