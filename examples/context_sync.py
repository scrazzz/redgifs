from redgifs import API # note this

with API() as api:
    response = api.search('latina', count=4)

print(response.gifs[0])  # pyright: ignore[reportOptionalSubscript]
