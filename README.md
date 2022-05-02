## redgifs

Async and Sync Python Wrapper for the RedGifs API.

> ⚠ **Note:** This project is still in development.

### Installation
```
pip install -U redgifs
```

`redgifs` works on Python versions 3.7 and above.

### Quickstart
Synchronous usage
```py
import redgifs

api = redgifs.API()
response = api.search('3D')
print(response)
api.close()
```

Asynchronous usage
```py
import asyncio
from redgifs.aio import API

async def main():
    api = API()
    response = await api.search('3D')
    print(response)
    await api.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

More examples can be found in the examples directory.

### Documentation
https://redgifs.readthedocs.io
