## redgifs

Async and Sync Python Wrapper for the RedGifs API.

> ⚠ **Note:** This project is still in development.

### Installation
The version on PyPi is not updated as of now. Please install using GitHub:
```
pip install -U git+https://github.com/scrazzz/redgifs
```

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
import redgifs.aio import API

async def main():
    api = API()
    response = await api.search('3D')
    print(response)
    await api.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### Documentation
https://redgifs.readthedocs.io
