<h1 align="center"> <code>redgifs</code> </h1>

<div align="center">
    <a href="https://pypi.org/project/redgifs">
        <img src="https://img.shields.io/pypi/v/redgifs.svg" alt="pypi">
    </a>
    <a href="https://github.com/scrazzz/redgifs/actions/workflows/test.yml">
        <img src="https://github.com/scrazzz/redgifs/actions/workflows/test.yml/badge.svg" alt="pytest">
    </a>
    <a href='https://redgifs.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/redgifs/badge/?version=latest' alt='Documentation Status' />
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

> [!IMPORTANT]
> - It is advised to install the [Development version](####development-version)  because v2.0 has a lot of bugs
> - A new v2.1 version will be released soon with major breaking changes

#### Development version
```
pip install -U git+https://github.com/scrazzz/redgifs
```

`redgifs` works on Python versions 3.8 and above.

-----

### Quickstart
#### 1. Command Line:

```console
$ redgifs --help
Usage: redgifs [OPTIONS] [URLS]...

Options:
  -q, --quality [sd|hd]  Video quality of GIF to download.  [default: hd]
  -d, --dir FOLDER_NAME  The folder/directory to save the downloads to.
  -i, --input PATH       Download URLs from a newline seperated txt file.
  -v, --version          Shows currently installed version.
  --help                 Show this message and exit
```

Examples:
```console
$ # Download files to a folder
$ ls
Home    Downloads  Homework  Music
Backup  Documents  Videos    Games
$ redgifs https://redgifs.com/watch/xyz --q sd --dir Homework
Downloading xyz...
Download complete
$ ls Homework
xyz.mp4
```

```console
$ # Download GIFs from a file that contains a list of URLs
$
$ # urls.txt:
$ # https://redigfs.com/watch/xyz
$ # https://redigfs.com/watch/qwe
$ # https://redigfs.com/watch/abc
$ # https://redigfs.com/watch/rst

$ redgifs -i urls.txt
Downloading xyz...
Download complete
Downloading qwe...
```

```console
$ # Download all GIFs from a user's profile
$ mkdir rg_vids
$ redgifs https://redgifs.com/users/usernamethatexists -d rg_vids
Downloaded 1/3 GIFs
Downloaded 2/3 GIFs
Downloaded 3/3 GIFs

Downloaded 3/3 videos of "usernamethatexists" to rg_vids folder sucessfully
```

#### 2. Synchronous usage:
```py
import redgifs

api = redgifs.API()
api.login() # Login with temporary token
response = api.search('3D')
print(response)
api.close()
```

#### 3. Asynchronous usage:
```py
import asyncio
from redgifs.aio import API # note this

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
- [Discord](https://discord.gg/NtAJMCcTd4)
- [Examples](https://github.com/scrazzz/redgifs/tree/main/examples)
