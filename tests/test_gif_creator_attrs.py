from redgifs import API, Tags
from redgifs.errors import HTTPException

def random_tag() -> str:
    return Tags().random(1)

def test_attrs():
    api = API()
    api.login()
    r = api.search(random_tag())

    if r.gifs is not None:
        username = r.gifs[0].username
        for gif in r.gifs:
            assert gif.id is not None
            assert gif.create_date
            assert isinstance(gif.has_audio, bool)
            assert gif.width and gif.height
            assert isinstance(gif.likes, int)
            assert gif.tags
            assert isinstance(gif.published, bool)
            assert gif.urls
        
        try:
            c = api.search_creator(username).creator
        except HTTPException as e:
            return print('Failed to get user profile. User may have been deleted.')

        # attrs commented out can be None or empty (str) or 0 (int)

        assert c.creation_time
        # assert c.description
        assert c.followers
        assert c.following >= 0
        assert c.gifs
        # assert c.links
        # assert c.name
        # assert c.poster
        # assert c.preview
        # assert c.profile_image_url
        # assert c.profile_url
        # assert c.published_collections
        assert c.published_gifs
        # assert c.status
        # assert c.subscription
        # assert c.thumbnail
        assert c.url
        assert c.username
        assert isinstance(c.verified, bool)
        assert c.views
