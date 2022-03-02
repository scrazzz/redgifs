## redgifs

Sync and Async Python Wrapper for RedGifs API.

> ⚠ **Note:** This Project is still in development.

### Installation
The version on PyPi is not updated as of now. Please install using GitHub:
```
pip install git+https://github.com/scrazzz/redgifs
```

### Quickstart
Synchronous usage
```py
import redgifs

from pprint import pprint

api = redgifs.API()
response = api.search('3D')
pprint(response, indent=3)
api.close()
```

Asynchronous usage
```py
import asyncio
import redgifs.aio import API

from pprint import pprint

async def main():
    api = API()
    response = await api.search('3D')
    pprint(response, indent=3)
    await api.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### Documentation
