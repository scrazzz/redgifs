"""
Example showing usage in an async code.
"""

from redgifs.aio import API
from redgifs import Order

import asyncio

async def main():
    api = API()
    await api.login()
    result = await api.search(
        'ass',
        order=Order.best, # Order it according to "best" (default: "recent")
        count=10,         # Min count is 10
        page=3            # Let's check the 3rd page
    )

    # Get the first gif from the results (if any)
    if result.gifs is not None:
        gif = result.gifs[0]
    else:
        return print(f'No results found for "{result.searched_for}"')

    # Print some information of the gif
    print(f'ID: {gif.id}', f'duration: {gif.duration}s', f'likes: {gif.likes}', sep=' | ')

    # Get the HD url of the gif
    print(gif.urls.hd)

    # Finally close the API session when you're done
    await api.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
