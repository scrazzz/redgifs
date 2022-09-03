.. currentmodule:: redgifs

Changelogs
==========

``[!]`` means it's a breaking change.

1.3.0
------
- Added :py:meth:`download() <redgifs.API.download()>` to download media from redgifs (GH `#7 <https://github.com/scrazzz/redgifs/issues/7>`_).
- Added :py:meth:`Tags.single_random() <redgifs.Tags.single_random()>` to get a single random tag.
- Added CLI support to download GIFs.
- Fixed some ``typing`` related errors.

1.2.0
------
- Added :py:class:`Image <redgifs.models.Image>`.
- Added ``images`` as new attribute for :py:class:`SearchResult <redgifs.models.SearchResult>`.
- Added :py:meth:`search_gif() <redgifs.API.search_gif()>` as an alias for :py:meth:`search() <redgifs.API.search()>`.
- Fixed some ``typing`` related errors.
- [!] Refactored :py:meth:`search_image() <redgifs.API.search_image()>` to return images in its proper dataclass.
- [!] :py:meth:`search() <redgifs.API.search()>` now returns Optional[:py:class:`SearchResult <redgifs.models.SearchResult>`].

1.1.0
------
- Added :py:class:`search_image() <redgifs.API.search_image()>` method.
- Added :py:class:`ProxyAuth <redgifs.http.ProxyAuth>` for proxy authentication.
- Fixed ``await`` calls (`#3 <https://github.com/scrazzz/redgifs/pull/3>`_).
- Fixed errors with Python 3.7.
- Refactored ``create_date`` and ``creation_time`` (`c95d8 <https://github.com/scrazzz/redgifs/commit/c95d8>`_).
- Refactored :py:class:`get_tags() <redgifs.API.get_tags()>` method.

1.0.0
-----
- Initial release.
