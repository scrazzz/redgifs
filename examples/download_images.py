"""
This example shows how to download images from RedGifs
"""

from redgifs import API

def main():
    # Login and initialise the API
    api = API().login()

    # You can refer the docs for additional params
    result = api.search_image(search_text='ava addams', count=15)

    # Get the images and save it as a variable
    images = result.images

    # If the search_text is invalid, or if RedGifs can't find what you are
    # looking for then this will be None.
    if images is None:
        print('No images found')
    else:
        # Print the image urls
        for img in images:
            print(img.urls.hd)

    # Finally close the API session
    api.close()

main()
