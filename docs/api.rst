.. currentmodule:: redgifs

API
---

API Instance
============

.. autoclass:: API
   :members:
   :member-order: bysource

Tags
====
A utility class for all things related to RedGifs tags.

.. autoclass:: Tags
   :members:
   :member-order: bysource

Proxy Auth
==========
A utility class to provide proxy authorization.

.. autoclass:: redgifs.ProxyAuth

Models
======
Models are classes that are received from Redgifs and are not meant to be created by the user of the library.

.. autoclass:: redgifs.models.URL()
   :members:

.. autoclass:: redgifs.models.GIF()
   :members:

.. autoclass:: redgifs.models.Image()
   :members:

.. autoclass:: redgifs.models.User()
   :members:

.. autoclass:: redgifs.models.SearchResult()
   :members:

.. autoclass:: redgifs.models.CreatorsResult()
   :members:

.. autoclass:: redgifs.models.CreatorResult()
   :members:


Enums
=====

.. autoclass:: Order
   :members:
   :undoc-members:


Exceptions
==========

.. autoexception:: RedGifsError

.. autoexception:: InvalidTag

.. autoexception:: HTTPException
