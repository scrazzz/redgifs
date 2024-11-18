from redgifs.api import API

def test_routes():
    api = API().login()
    # assert api.get_feeds() # removed on v2.0.0
    assert api.get_tags()
    assert api.get_top_this_week()
    assert api.get_trending_gifs()
    assert api.get_trending_images()
    assert api.get_trending_tags()
    assert api.fetch_tag_suggestions('mia malkova')
