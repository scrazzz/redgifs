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

from typing import Any, Union

class RedgifsError(BaseException):
    """Base class for all redgifs error"""
    pass

class NoMatchFound(RedgifsError):
    """Exception raised when no match was found.
    
    Attributes
    ----------
    query: :class:`str`
        The query that was searched for.
    """
    def __init__(self, query: str):
        self.query: str = query
        super().__init__(f'Match for "{query}" was not found')

class HTTPException(RedgifsError):
    """Exception raised when an HTTP Exception occurs.

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The response of the failed HTTP request.

    status: :class:`int`
        The status code of the HTTP request.

    error: :class:`str`
        The original error message from RedGifs.
    """

    def __init__(self, response: Union[requests.Response, aiohttp.ClientResponse], json: Union[dict, str], _async: bool = False):
        self.response: Any = response
        self.status: int = response.status if _async else response.status_code
        self.error: str = json
        if isinstance(json, dict):
            self.error = json.get('errorMessage')
        
        super().__init__(f'{self.status} {self.reason} (Error: {self.error})')
