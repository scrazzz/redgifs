"""
This example shows how you can use the Tag enum
for searching for gifs. Not the best way to search.
"""

from redgifs import API, Tags

api = API()
# Helpful to find a tag if you're using an IDE with autocomplete
result = api.search(Tags.brunette)
print(result.total)
