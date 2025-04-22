import pytest
from redgifs import API, Tags

@pytest.mark.parametrize(
    'query',
    Tags().random(7)
)
def test_attrs(query):
    api = API()
    api.login()
    r = api.search_image(query)

    if r.images is not None:
        for img in r.images:
            assert img.id
            assert img.create_date
            assert img.width
            assert img.height
            # assert img.likes
            assert img.tags
            # assert img.verified
            assert img.views
            assert img.published
            assert img.urls
            assert img.username
            assert img.type
            assert img.avg_color
