```{eval-rst}
.. currentmodule:: redgifs
```

# API

## API Instance

```{eval-rst}
.. autoclass:: API
   :members:
   :member-order: bysource
```

## Async API

Same as {ref}`API` but for usage in async context.

```{eval-rst}
.. autoclass:: redgifs.aio.API
   :members:
   :member-order: bysource
```

## Tags

A utility class for all things related to RedGifs tags.

```{eval-rst}
.. autoclass:: Tags
   :members:
   :member-order: bysource
```

## Proxy Auth

A utility class to provide proxy authorization.

```{eval-rst}
.. autoclass:: redgifs.ProxyAuth
```

## Models

Models are classes that are received from Redgifs and are not meant to be created by the user of the library.

```{eval-rst}
.. autoclass:: redgifs.models.URL()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.GIF()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.Image()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.User()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.Feeds()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.SearchResult()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.CreatorsResult()
   :members:
```

```{eval-rst}
.. autoclass:: redgifs.models.CreatorResult()
   :members:
```

## Enums

```{eval-rst}
.. autoclass:: Order
   :members:
   :undoc-members:
```

## Exceptions

```{eval-rst}
.. autoexception:: RedGifsError
```

```{eval-rst}
.. autoexception:: InvalidTag
```

```{eval-rst}
.. autoexception:: HTTPException
```
