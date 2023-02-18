.. currentmodule:: redgifs

Changelogs
==========

1.6.0
-----

**Breaking changes**

- Renamed ``RedgifsError`` to :py:class:`RedGifsError <redgifs.errors.RedGifsError>`.
- Changed return type of :py:attr:`duration <redgifs.models.GIF.duration>` as ``int`` instead of ``float``.

**Updates**

- Improved CLI.

Now you can run ``redgifs`` in your terminal to use the CLI. See ``redgifs -h`` for help.

- Fixed thumbnail regex (`4c3606b <https://github.com/scrazzz/redgifs/commit/4c3606b>`_).

1.5.1
-----
- Properly fixed an issue with CLI downloads.

1.5.0
-----
- Added new method: :py:meth:`get_trending_tags() <redgifs.API.get_trending_tags()>`
- Added new method: :py:meth:`fetch_tag_suggestions() <redgifs.API.fetch_tag_suggestions()>`.
- Added new method: :py:meth:`search_creator() <redgifs.API.search_creator>`. Alias: :py:meth:`search_user() <redgifs.API.search_user()>`
- Added new dataclass :py:class:`CreatorResult <redgifs.models.CreatorResult>`.
- Fixed :py:meth:`download() <redgifs.API.download()>` method not working in async context.
- Fixed :py:meth:`search_creators() <redgifs.API.search_creators()>` method error.
- Fixed an error regarding authorization for CLI.

1.4.0
-----

**Breaking changes**

- Dropped support for Python version 3.7.

**Updates**

- Added :py:meth:`login() <redgifs.API.login()>` for logging in with a temporary token.
- Fixed errors with API requiring a token. See above added feature.
- Fixed error message sometimes returning "None".

1.3.1
-----
- Added ``--version`` argument in ``__main__.py`` file.

1.3.0
------

**Breaking changes**

- :py:meth:`Tags.search() <redgifs.Tags.search()>` now returns a list of closest tag names.

**Updates**

- Added ``web_url`` attribute to :py:meth:`GIF <redgifs.models.GIF()>`.
- Added :py:meth:`download() <redgifs.API.download()>` to download media from redgifs (GH `#7 <https://github.com/scrazzz/redgifs/issues/7>`_).
- Added :py:meth:`Tags.single_random() <redgifs.Tags.single_random()>` to get a single random tag.
- Added CLI support to download GIFs.
- Fixed an issue with HTTP timeout (GH `#9 <https://github.com/scrazzz/redgifs/issues/9>`_).
- Fixed some ``typing`` related errors.
- Renamed ``Gif`` dataclass to :py:class:`GIF <redgifs.models.GIF>`.

1.2.0
------

**Breaking changes**

- Refactored :py:meth:`search_image() <redgifs.API.search_image()>` to return images in its proper dataclass.
- :py:meth:`search() <redgifs.API.search()>` now returns Optional[:py:class:`SearchResult <redgifs.models.SearchResult>`].

**Updates**

- Added :py:class:`Image <redgifs.models.Image>`.
- Added ``images`` as new attribute for :py:class:`SearchResult <redgifs.models.SearchResult>`.
- Added :py:meth:`search_gif() <redgifs.API.search_gif()>` as an alias for :py:meth:`search() <redgifs.API.search()>`.
- Fixed some ``typing`` related errors.

1.1.0
------
- Added :py:meth:`search_image() <redgifs.API.search_image()>` method.
- Added :py:class:`ProxyAuth <redgifs.http.ProxyAuth>` for proxy authentication.
- Fixed ``await`` calls (`#3 <https://github.com/scrazzz/redgifs/pull/3>`_).
- Fixed errors with Python 3.7.
- Refactored ``create_date`` and ``creation_time`` (`c95d8 <https://github.com/scrazzz/redgifs/commit/c95d8>`_).
- Refactored :py:class:`get_tags() <redgifs.API.get_tags()>` method.

1.0.0
-----
- Initial release.
