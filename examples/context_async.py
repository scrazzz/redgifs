import asyncio
from redgifs.aio import API # note this

async def main():
    async with API() as api:
        response = await api.search('latina', count=4)

    print(response.gifs[0])  # pyright: ignore[reportOptionalSubscript]


# MAIN
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
