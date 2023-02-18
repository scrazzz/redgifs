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

import requests
import aiohttp

from typing import Any, Dict, Optional, Union

class RedGifsError(BaseException):
    """Base class for all redgifs errors."""
    pass

class InvalidTag(RedGifsError):
    """Exception raised when no match was found for a tag.

    Attributes
    ----------
    tag: :class:`str`
        The tag that was searched for.
    """
    def __init__(self, tag: str):
        self.tag: str = tag
        super().__init__(f'Tag for "{tag}" was not found.')

class HTTPException(RedGifsError):
    """Exception raised when an HTTP Exception occurs.

    Attributes
    ----------
    response: Union[:class:`requests.Response`, :class:`aiohttp.ClientResponse`]
        The response of the failed HTTP request. It may be either :class:`requests.Response` or :class:`aiohttp.ClientResponse`.
    status: :class:`int`
        The status code of the HTTP request.
    error: :class:`str`
        The original error message from RedGifs.
    """

    def __init__(self, response: Union[requests.Response, aiohttp.ClientResponse], json: Optional[Union[Dict[str, Any], str]]):
        self.response: Any = response

        if isinstance(response, requests.Response):
            self.status = response.status_code
        elif isinstance(response, aiohttp.ClientResponse):
            self.status = response.status

        self.error: Optional[Union[Dict[str, Any], str]] = json
        if isinstance(json, dict):
            self.error = json.get('errorMessage') or json.get('error')

        super().__init__(f'{self.status} (Error: {self.error})')
