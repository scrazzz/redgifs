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

__title__ = 'redgifs'
__author__ = 'scrazzz'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2022-present scrazzz'
__version__ = '2.3.0'

from typing import Literal, NamedTuple

from .api import *
from .http import *
from .enums import *
from .tags import *
from .errors import *
from .utils import *

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal['alpha', 'beta', 'final']

version_info: VersionInfo = VersionInfo(major=2, minor=3, micro=0, releaselevel='final')

del NamedTuple, VersionInfo
