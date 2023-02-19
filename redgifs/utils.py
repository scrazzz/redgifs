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
import yarl

from .const import REDGIFS_THUMBS_RE, IP_ADDR_RE

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
    u = yarl.URL(url)
    if u.query.get('for'):
        for_value = re.sub(IP_ADDR_RE, 'REDACTED', u.query['for'])
        return u % {'for': for_value}
    return url
