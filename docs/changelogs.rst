.. currentmodule:: redgifs

Changelogs
==========

2.3.0
-----
- Fixed CLI download logic and f-string error `0af610a <https://github.com/scrazzz/redgifs/commit/0af610a6d0f30a2f93a5c95c1dc0166000d2eef7>`_
- Changed type of :py:attr:`.URL.thumbnail` to ``Optional[str]``

2.2.0
-----
- Fixed multiple KeyErrors inside the library:

  * https://github.com/scrazzz/redgifs/commit/c4acb0d1a8f0c8bce558c398c9b1e9e17d0f397b
  * https://github.com/scrazzz/redgifs/commit/e654b1b2ecbad7f5cc06f459deb60a5093a3bd7d
  * https://github.com/scrazzz/redgifs/commit/13ca04479c2ec8b4d9f8b56e1dbb8e3ddec1a6ae
  * https://github.com/scrazzz/redgifs/commit/e654b1b2ecbad7f5cc06f459deb60a5093a3bd7d

- Fixed KeyError in :py:meth:`.Tags.random()` method when used independently.
- Changed type of :py:attr:`.User.profile_url`
- Changed type of :py:attr:`.User.name`
- Changed type of :py:attr:`.URL.hd`

2.1.1
-----
- Removed usage of deprecated :class:`.Order` inside the library.
- Added required ``click`` dependency in ``pyproject.toml``.
- Fixed issue `#45 <https://github.com/scrazzz/redgifs/issues/45>`_.

2.1.0
-----

**Breaking Changes**

- From this version onwards, breaking changes will be done on "minor" versions (semver ``major.minor.patch``).
- Please refer to the migrating guide (:ref:`Migrating to v2.x`) to know about the changes on this version.

2.0.0
-----

**Major Breaking Changes**

- See :ref:`Migrating to v2.x`

1.9.4
-----
- Updated redgifs CLI. Check the GitHub README for more info.

1.9.3
-----
- Upated ``tags.json`` with new tags. You can access them from :py:meth:`Tags.search() <redgifs.Tags.search>`.


1.9.2
-----
- Upated ``tags.json`` with new tags. You can access them from :py:meth:`Tags.search() <redgifs.Tags.search>`.

1.9.1
-----
- :py:attr:`URL.file_url <redgifs.models.URL.file_url>` is deprecated and will be removed in v2.0, use :py:attr:`URL.embed_url <redgifs.models.URL.embed_url>` instead.

1.9.0
-----
- Fixed an issue with CLI not downloading the last page of the user's gifs.
- Added new :py:meth:`API.get_top_this_week() <redgifs.API.get_top_this_week()>` method.
- Added proper types to the API responses.

Many issues were found and fixed.

- The type of certain attributes were changed. E.g (:py:attr:`GIF.duration <redgifs.models.GIF.duration>` was changed from ``int`` to ``float``).
- Certain attributes were returning invalid data which were fixed. E.g: (`5765501 <https://github.com/scrazzz/redgifs/commit/5765501#diff-e4a15e908eff2a2d37a9274961771a9e8bfa434bc7b11e7e2de396be0855925dR199>`_).

1.8.2
-----
- Added new keyword argument ``type`` to :py:meth:`API.search_creator() <redgifs.API.search_creator()>` method. This allows for getting images and gifs of the creator seperately.
- Added new :py:attr:`images <redgifs.models.CreatorResult.images>` parameter for :py:class:`CreatorResult <redgifs.models.CreatorResult>`.

1.8.1
------
- Fixed an issue with CLI not downloading GIFs using the ``--list`` option.

1.8.0
-----

**Breaking changes**

- Removed ``username`` and ``password`` params from :py:meth:`login() <redgifs.API.login()>` method.
- Changed return type of :py:meth:`login() <redgifs.API.login()>` method from :py:class:`bool` to :py:class:`API <redgifs.API>`.
- Changed return type of :py:meth:`Tags.random() <redgifs.Tags.random()>` method.

**Updates**
- Added new :py:attr:`Order.new <redgifs.Order.new>` enum.

1.7.2
-----
- Added new :py:attr:`links <redgifs.models.User.links>` attribute to :py:class:`User <redgifs.models.User>`.
- Added new :py:meth:`get_trending_gifs() <redgifs.API.get_trending_gifs()>` method.
- Added new :py:meth:`get_trending_images() <redgifs.API.get_trending_images()>` method.

1.7.1
-----
- Added new :py:attr:`file_url <redgifs.models.URL.file_url>` attribute to :py:class:`URL <redgifs.models.URL>`. This can be displayed to the end user since it doesn't have any IP or signature info in the URL.
- Added new :py:meth:`get_feeds() <redgifs.API.get_feeds()>` method.
- Added new :py:class:`Feeds <redgifs.models.Feeds>` dataclass.

1.7.0
-----

**Breaking changes**

- Removed ``Tags`` enum class.

The ``Tag`` enum has been removed in place of a new :py:class:`Tag <redgifs.tags.Tags>` class.
This makes it easier to use the newest tags that are available on RedGifs instead of updating the enum everytime.

**Updates**

- Changed the default ``order`` paramter of :py:meth:`search_image() <redgifs.API.search_image()>` from ``Order.trending`` to ``Order.new``.

1.6.1
-----
- Changed default ``order`` paramter of :py:meth:`search() <redgifs.API.search()>` to :py:attr:`Order.trending <redgifs.Order.trending>`.
- Added ``count`` paramter to :py:meth:`search_creator() <redgifs.API.search_creator()>`.
- Added :py:attr:`new <redgifs.Order.new>` value to :py:class:`Order <redgifs.Order>` enum.
- Added :py:attr:`gifs <redgifs.models.CreatorResult.gifs>` attribute to :py:class:`CreatorResult <redgifs.models.CreatorResult>`.
- Added new ``--folder`` option in redgifs CLI. Use this option to download the video(s) to a folder/directory.
- Added new feature to download all videos from a RedGifs profile using redgifs CLI. Just enter the user's profile URL to the ``[URL]`` paramter. 
- Added new ``--quality`` option to redgifs CLI.

1.6.0
-----

**Breaking changes**

- Renamed ``RedgifsError`` to :py:class:`RedGifsError <redgifs.errors.RedGifsError>`.
- Changed return type of :py:attr:`duration <redgifs.models.GIF.duration>` to ``int`` instead of ``float``.

**Updates**

- Improved CLI. Now you can run ``redgifs`` in your terminal to use the CLI. See ``redgifs -h`` for help.
- Fixed thumbnail regex (`4c3606b <https://github.com/scrazzz/redgifs/commit/4c3606b>`_).

1.5.1
-----
- Properly fixed an issue with CLI downloads.

1.5.0
-----
- Added new method: :py:meth:`get_trending_tags() <redgifs.API.get_trending_tags()>`
- Added new method: :py:meth:`fetch_tag_suggestions() <redgifs.API.fetch_tag_suggestions()>`.
- Added new method: :py:meth:`search_creator() <redgifs.API.search_creator>` and alias :py:meth:`search_user() <redgifs.API.search_user()>`
- Added new dataclass :py:class:`CreatorResult <redgifs.models.CreatorResult>`.
- Fixed :py:meth:`download() <redgifs.API.download()>` method not working in async context.
- Fixed :py:meth:`search_creators() <redgifs.API.search_creators()>` method error.
- Fixed an error regarding authorization for CLI.

1.4.0
-----

**Breaking changes**

- Dropped support for Python version 3.7.

**Updates**

- Added :py:meth:`login() <redgifs.API.login()>` method for logging in with a temporary token.
- Fixed errors with API requiring a token. See above added feature.
- Fixed error message sometimes returning "None".

1.3.1
-----
- Added ``--version`` argument in ``__main__.py`` file (for CLI usage).

1.3.0
------

**Breaking changes**

- Renamed ``Gif`` dataclass to :py:class:`GIF <redgifs.models.GIF>`.
- :py:meth:`Tags.search() <redgifs.Tags.search()>` now returns a list of closest tag names.

**Updates**

- Added ``web_url`` attribute to :py:meth:`GIF <redgifs.models.GIF()>`.
- Added :py:meth:`download() <redgifs.API.download()>` to download media from redgifs (GH `#7 <https://github.com/scrazzz/redgifs/issues/7>`_).
- Added :py:meth:`Tags.single_random() <redgifs.Tags.single_random()>` to get a single random tag.
- Added CLI support to download GIFs.
- Fixed an issue with HTTP timeout (GH `#9 <https://github.com/scrazzz/redgifs/issues/9>`_).
- Fixed some ``typing`` related errors.

1.2.0
------

**Breaking changes**

- Refactored :py:meth:`search_image() <redgifs.API.search_image()>` method to return images in its proper dataclass.
- :py:meth:`search() <redgifs.API.search()>` now returns Optional[:py:class:`SearchResult <redgifs.models.SearchResult>`].

**Updates**

- Added new :py:class:`Image <redgifs.models.Image>` dataclass.
- Added new :py:attr:`images <redgifs.models.SearchResult.images>` attribute for :py:class:`SearchResult <redgifs.models.SearchResult>`.
- Added :py:meth:`search_gif() <redgifs.API.search_gif()>` method as an alias for :py:meth:`search() <redgifs.API.search()>`.
- Fixed some ``typing`` related errors.

1.1.0
------
- Added new :py:meth:`search_image() <redgifs.API.search_image()>` method.
- Added :py:class:`ProxyAuth <redgifs.http.ProxyAuth>` for proxy authentication. Check the examples in the repo for use.
- Fixed ``await`` calls (`#3 <https://github.com/scrazzz/redgifs/pull/3>`_).
- Fixed errors with Python 3.7.
- Refactored ``create_date`` and ``creation_time`` (`c95d8 <https://github.com/scrazzz/redgifs/commit/c95d8>`_).
- Refactored :py:class:`get_tags() <redgifs.API.get_tags()>` method.

1.0.0
-----
- Initial release.
