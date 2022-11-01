"""
Example showing usage in sync code.
"""

import redgifs
from redgifs import Order

api = redgifs.API()
api.login()
result = api.search(
    'japanese',
    order=Order.trending, # Order it according to "trending" (default: "recent")
    count=10,             # Min count is 10
    page=5                # Let's check the 5th page
)

# Get the first gif from the results (if any)
if result.gifs is not None:
    gif = result.gifs[0]
else:
    print(f'No gifs found for "{result.searched_for}"')
    exit(1)

# Print some information of the gif
print(f'ID: {gif.id}', f'duration: {gif.duration}s', f'likes: {gif.likes}', sep=' | ')

# Get the SD url of the gif
print(gif.urls.sd)

# Finally close the API session when you're done
api.close()
