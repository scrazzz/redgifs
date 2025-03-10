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

# TODO: Deprecate lower-case enum members @ v2.2
import warnings
from enum import Enum, EnumMeta

__all__ = ('Order', 'MediaType')

class OrderMeta(EnumMeta):
    """Custom metaclass to handle deprecated enum attributes."""
    def __getattribute__(cls, name: str):
        """Intercept class attribute access to raise warnings for deprecated names."""
        deprecated_names = {
            "trending", "top", "latest", "oldest", "recent", "best", "top28", "new"
        }
        if name in deprecated_names:
            warnings.warn(
                f"'Order.{name}' is deprecated, use 'Order.{name.upper()}' instead.",
                DeprecationWarning,
                stacklevel=2
            )
        return super().__getattribute__(name)

class Order(Enum, metaclass=OrderMeta):
    """An enum representing the order of the results."""

    TRENDING = 'trending'
    trending = 'trending'
    TOP = 'top'
    top = 'top'
    LATEST = 'latest'
    latest = 'latest'
    OLDEST = 'oldest'
    oldest = 'oldest'

    # These tags are not available on the web UI but still works through the API.
    RECENT = 'recent'
    recent = 'recent'
    BEST = 'best'
    best = 'best'
    TOP28 = 'top28'
    top28 = 'top28'
    NEW = 'new'
    new = 'new'

class MediaType(Enum):
    """An enum representing the media type of the results."""
    IMAGE = 'i'
    GIF = 'g'
