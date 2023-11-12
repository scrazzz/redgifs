"""
This example shows how you can download all GIFs from a user's profile on RedGifs.
"""

from redgifs import API

api = API()
api.login()

# Search for the user
USERNAME = 'enter_username_here'
data = api.search_creator(USERNAME)

total_pages = data.pages
current_page = data.page

# This is the total gifs in the `current_page`
total_gifs = data.gifs

while current_page <= total_pages:
    for i, gifs in enumerate(total_gifs, start=1):
        try:
            # We do the downloading here.
            # Make sure you have a folder called "downloads" in the current directory or else make a new one.
            api.download(gifs.urls.hd, f'downloads/{i}.mp4')

            # Print a message to keep track of the downloads
            print(f'Downloaded {i} out of {data.total}')

        except Exception as e:
            raise Exception(f'An error occured while donwloading:\n{e}')

    # If we are in the last page, break the while loop
    if current_page == total_pages:
        break

    # otherwise, we continue...

    # Update the current page number
    current_page += 1
    # Clear the old gifs from the previous page
    total_gifs.clear()
    # Make a new API call to get the gifs from the next page
    data = api.search_creator(USERNAME, page=current_page)
    # Update `total_gifs` with the new gifs
    total_gifs.extend(data.gifs)

print('Completed!')
