.. currentmodule:: redgifs

Migrating to v2.0
#################
v2.0 has some breaking changes due to how volatile the interal RedGifs API is. Also it has been some time since the last update :)

Changes
*******
Below are the breaking changes to v2.0. If you had any methods or code related to the below mentioned items, you should update your code to reflect the new changes.

Feeds API
---------
The entire feeds API has been removed. RedGifs had removed the feeds page from the website a long time ago and is no longer required.

* This means the following methods/attributes have been removed:

  * ``API.get_feeds()`` method (from both sync and async codebase).

  * ``Feeds`` dataclass.

  * ``parse_feeds()`` internal helper method.

Poster URL
----------
:py:attr:`URLs.poster <redgifs.models.URLs.poster>` now returns ``Optional[str]`` instead of ``str``. It has been observed that not all posters are available always.

Updates
*******
General updates to the library.

- Upated ``tags.json`` with new tags. You can access them from :py:meth:`Tags.search() <redgifs.Tags.search>`.
- [CLI] GIFs can now be downloaded by just providing the ID of the GIF.
