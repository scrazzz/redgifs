"""
This example shows how to use tags for searching.

Only use this if you really need to, otherwise just search 
the normal way (take a look at the main example in the README).
"""

from redgifs import API, Tags

def main():
    # Login to the RedGifs API
    api = API().login()

    # Create an instance of Tags
    tags = Tags()

    # Here we input the search term. The result is a list of tags with the closest tag name.
    # You could use this if you are taking in a user input or looking up specific creators but don't
    # know their proper spelling, etc..
    # This will error if it can't find a proper tag.
    query = tags.search('search term here')[0]

    # Using the query:
    result = api.search_gif(query)
    print(result.gifs)

if __name__ == '__main__':
    main()
