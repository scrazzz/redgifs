.. currentmodule:: redgifs

Migrating to v2.x
#################
v2.x has some breaking changes due to how volatile the interal RedGifs API is. *Also it has been a while since the last update :)*

-----

Breaking Changes
****************
Below mentions the breaking changes on v2.x. If you had any methods or code related to the below mentioned items, you should update your code to reflect the new changes.

1. Feeds API
------------
The entire feeds API has been removed. RedGifs had removed the feeds page from the website a long time ago so this API being in the library is pointless.

* This means the following methods/attributes have been removed:

  * ``API.get_feeds()`` method (from both sync and async codebase).
  * ``Feeds`` dataclass.
  * ``parse_feeds()`` internal helper method.

2. Poster URL
-------------
:attr:`.URL.poster` now returns Optional[:class:`str`] instead of :class:`str`.

3. Tag Suggestions
------------------
The :meth:`~redgifs.API.fetch_tag_suggestions()` method has been updated and now returns a List[:class:`.TagSuggestion`] type.

4. :class:`MediaType` enum
--------------------------
The enum which was passed to methods :meth:`~redgifs.API.get_top_this_week()` and :meth:`~redgifs.API.search_creator()`
has been renamed from ``Type`` to :class:`.MediaType`.

.. code:: diff

    from redgifs import API
    -from redgifs import Type
    +from redgifs import MediaType

    api = redgifs.API().login()
    -api.search_creator('username', type=Type.image)
    +api.search_creator('username', type=MediaType.IMAGE)

5. :class:`.Order` enum
-----------------------
In v2.1 the enum members were changed to uppercase which follows the PEP8 guidelines.
Lowercase enums will continue to work until v2.2 but will throw a DeprecationWarning if used.
It is advised to switch to the uppercase enum members (e.g, ``Order.BEST``, ``Order.LATEST``) asap.

6. CLI
------
The CLI option ``--dir`` (``-d``) has been renamed to ``--folder`` (``-f``).

-----

Updates
*******
General fixes/updates to the library.

v2.0

- Fixed unreachable code (`257ca39 <https://github.com/scrazzz/redgifs/commit/257ca39>`_).
- Added new tags. You can access them from :py:meth:`Tags.search() <redgifs.Tags.search>`.
- [CLI] GIFs can now be downloaded by just providing the ID of the GIF.

v2.1

- Fix an internal ``KeyError`` that occurs rarely when using :meth:`~redgifs.API.search_creator()`.
- Added :attr:`.embed_url` to images.
- [CLI] Fix CLI not acknowledging valid RedGifs URLs.
- [CLI] Added support to download images of a creator.
