"""
This example shows how to download GIFs from RedGIFs using this library.
"""

from redgifs import API

api = API()
api.login()

# Here we are searching for a GIF and only returning 15 of it.
count = 10
result = api.search_gif('hitomi tanaka', count=count)

# Check if your searched GIF exists.
# If not, print an error message and halt the program.
if result.gifs is None:
    print(f'No results found for {result.searched_for}')
    exit(1)


# Here we are downloading the gifs in the current directory.
# If you want to move it to a specific directory, then make sure you have
# created that folder first and use "/dir_name/video{n}.mp4" where dir_name is
# the folder that you have created.
n = 1
for gif in result.gifs:
    api.download(gif.urls.hd, f'video{n}.mp4')
    # It's good to see where we are at while this is downloading.
    print(f'Downloading {n}/{count}')
    # Increment the number after a download is complete to keep
    # track of the total downloaded GIFs.
    n += 1

print('Download complete')
