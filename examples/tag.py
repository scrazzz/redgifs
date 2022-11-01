"""
This example shows how you can use the Tag enum
for searching for gifs. Not the best way to search.
"""

from redgifs import API, Tags

api = API()
api.login()

# Helpful to find a tag if you're using an IDE with autocomplete.
result = api.search(Tags.brunette)

# If you want to search manually, use Tags.search which returns a
# list of closest tag names associated to it.
tags = Tags.search('autumn falls')
result = api.search(tags[0])  # Get the 1st one from the list of closest tag names

# If you want to get a random tag.
# This will give you 4 random Tags.
tags = Tags.random(count=4)
result = api.search(tags[2])  # Get the 3rd random tag

# Sometimes you just want a single random tag.
# You could to the above method and use "tags[0]" to get it or alternatively:
tag = Tags.single_random()
result = api.search(tag)
