from redgifs import API

def test_attrs():
    api = API()
    api.login()
    r = api.search('slim')

    if r.gifs is not None:
        for gif in r.gifs:
            assert gif.id is not None
            assert gif.create_date
            assert type(gif.has_audio) is bool
            assert gif.width and gif.height
            assert type(gif.likes) is int
            assert gif.tags
            assert type(gif.published) is bool
            assert gif.urls