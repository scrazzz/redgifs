<h1 align="center"> <code>redgifs</code> </h1>

<div align="center">
    <a href="https://pypi.org/project/redgifs">
        <img src="https://img.shields.io/pypi/v/redgifs.svg" alt="pypi">
    </a>
    <a href="https://github.com/scrazzz/redgifs/actions/workflows/test.yml">
        <img src="https://github.com/scrazzz/redgifs/actions/workflows/test.yml/badge.svg" alt="pytest">
    </a>
</div>

<p align="center"> Async and Sync Python Wrapper for the RedGIFs API. </p>

-----

> ⭐ _Please star this repo to support the developer and to encourage the development of this project!_

-----

### Installation
```
pip install -U redgifs
```

#### Development version
```
pip install -U git+https://github.com/scrazzz/redgifs
```

`redgifs` works on Python versions 3.8 and above.

-----

### Quickstart
Command Line:
`redgifs --help`
```console
usage: redgifs [-h] [--folder FOLDER] [--list FILE] [--version] [--quality QUALITY] [URL]

positional arguments:
  URL                Enter a RedGifs URL

options:
  -h, --help         show this help message and exit
  --folder FOLDER    Folder to download the video(s) to.
  --list FILE        Download GIFs from a txt file containing URLs seperated by a newline.
  --version          Show redgifs version info.
  --quality QUALITY  The video quality of the GIF to download. Available options are: "sd" and "hd".
```

Synchronous usage:
```py
import redgifs

api = redgifs.API()
api.login() # Login with temporary token
response = api.search('3D')
print(response)
api.close()
```

Asynchronous usage:
```py
import asyncio
from redgifs.aio import API

async def main():
    api = API()
    await api.login() # Login with temporary token
    response = await api.search('3D')
    print(response)
    await api.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

More examples can be found in the examples directory.

-----

### Links
- [Documentation](https://redgifs.readthedocs.io)
- [Discord](https://discord.gg/yNsUTuXvzn)
