.. currentmodule:: redgifs

Migrating to v2.0
#################
v2.0 has some breaking changes due to how volatile the interal RedGifs API is. *Also it has been a while since the last update :)*

Breaking Changes
****************
Below mentions the breaking changes on v2.0. If you had any methods or code related to the below mentioned items, you should update your code to reflect the new changes.

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


Updates
*******
General updates to the library.

- Fixed unreachable code (`257ca39 <https://github.com/scrazzz/redgifs/commit/257ca39>`_).
- Added new tags. You can access them from :py:meth:`Tags.search() <redgifs.Tags.search>`.
- [CLI] GIFs can now be downloaded by just providing the ID of the GIF.
