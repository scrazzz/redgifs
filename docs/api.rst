.. currentmodule:: redgifs

API
---

API Instance
============

.. autoclass:: API
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

.. autoclass:: redgifs.models.Gif()
   :members:

.. autoclass:: redgifs.models.Image()
   :members:

.. autoclass:: redgifs.models.User()
   :members:

.. autoclass:: redgifs.models.SearchResult()
   :members:

.. autoclass:: redgifs.models.CreatorsResult()
   :members:

Enums
=====

.. autoclass:: Order
   :members:
   :undoc-members:

.. autoclass:: Tags
   :noindex:
   :members:

.. autoclass:: Tags
   :members:
   :undoc-members:


Exceptions
==========

.. autoexception:: RedgifsError

.. autoexception:: InvalidTag

.. autoexception:: HTTPException
