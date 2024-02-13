from redgifs import API

def test_attrs():
    api = API()
    api.login()
    r = api.search('slim')

    if r.gifs is not None:
        for gif in r.gifs:
            assert gif.id is not None
            assert gif.create_date
            assert isinstance(gif.has_audio, bool)
            assert gif.width and gif.height
            assert isinstance(gif.likes, int)
            assert gif.tags
            assert isinstance(gif.published, bool)
            assert gif.urls
