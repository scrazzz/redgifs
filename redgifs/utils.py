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

import re
import json
import pkgutil
import asyncio
from typing import Dict

from yarl import URL

from .const import REDGIFS_THUMBS_RE

def _to_web_url(id_or_url: str, use_regex: bool = False) -> str:
    if not use_regex:
        return f'https://redgifs.com/watch/{id_or_url.lower()}'

    match = re.match(REDGIFS_THUMBS_RE, id_or_url)
    if not match:
        return ''

    try:
        id = match.group('id')
        return f'https://redgifs.com/watch/{id.lower()}'
    except IndexError:
        return ''

def strip_ip(url: str) -> str:
    u = URL(url)
    if u.query.get('for'):
        return str(u % {'for': 'REDACTED'})
    return url

def build_file_url(url: str) -> str:
    # use the 'sd' url here
    u = URL(url)
    filename = u.path.replace('/', '').replace('-mobile.mp4', '')
    return f'https://api.redgifs.com/v2/gifs/{filename.lower()}/files/{filename}.mp4'

def _read_tags_json() -> Dict[str, str]:
    file_ = pkgutil.get_data(__name__, 'tags.json') # type: ignore - We know this won't be None
    return json.loads(file_) # type: ignore - same reason above

async def _async_read_tags_json() -> Dict[str, str]:
    r = await asyncio.get_event_loop().run_in_executor(None, _read_tags_json)
    return r
