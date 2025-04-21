from redgifs import API, Order

api = API().login()

# GIFS
def test_order_recent():
    r = api.search('big ass', order=Order.RECENT)
    assert r

# def test_order_followers():
#     r = api.search('big dick', order=Order.followers)
#     assert r

def test_order_best():
    r = api.search('big tits', order=Order.BEST)
    assert r

def test_order_trending():
    r = api.search('hitomi tanaka', order=Order.TRENDING)
    assert r

def test_order_top28():
    r = api.search('hitomi tanaka', order=Order.TOP28)
    assert r

def test_order_new():
    r = api.search('ava addams', order=Order.NEW)
    assert r

def test_order_latest():
    r = api.search('violet myers', order=Order.LATEST)
    assert r

def test_order_oldest():
    r = api.search('mia khalifa', order=Order.OLDEST)
    assert r

# ----------------------------- #

# IMAGES
def test_order_recent_i():
    r = api.search_image('big ass', order=Order.RECENT)
    assert r

def test_order_best_i():
    r = api.search_image('big tits', order=Order.BEST)
    assert r

def test_order_trending_i():
    r = api.search_image('hitomi tanaka', order=Order.TRENDING)
    assert r

def test_order_top28_i():
    r = api.search_image('dee williams', order=Order.TOP28)
    assert r

def test_order_new_i():
    r = api.search_image('ava addams', order=Order.NEW)
    assert r

def test_order_latest_i():
    r = api.search_image('violet myers', order=Order.LATEST)
    assert r

def test_order_oldest_i():
    r = api.search_image('mia khalifa', order=Order.OLDEST)
    assert r
