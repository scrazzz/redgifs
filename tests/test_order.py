from redgifs import API, Order, Tags

api = API().login()

def random_tag() -> str:
    return Tags().random(1)


# GIFS
def test_order_recent():
    r = api.search(random_tag(), order=Order.RECENT)
    assert r

def test_order_best():
    r = api.search(random_tag(), order=Order.BEST)
    assert r

def test_order_trending():
    r = api.search(random_tag(), order=Order.TRENDING)
    assert r

def test_order_top28():
    r = api.search(random_tag(), order=Order.TOP28)
    assert r

def test_order_new():
    r = api.search(random_tag(), order=Order.NEW)
    assert r

def test_order_latest():
    r = api.search(random_tag(), order=Order.LATEST)
    assert r

def test_order_oldest():
    r = api.search(random_tag(), order=Order.OLDEST)
    assert r

# ----------------------------- #

# IMAGES
def test_order_recent_i():
    r = api.search_image(random_tag(), order=Order.RECENT)
    assert r

def test_order_best_i():
    r = api.search_image(random_tag(), order=Order.BEST)
    assert r

def test_order_trending_i():
    r = api.search_image(random_tag(), order=Order.TRENDING)
    assert r

def test_order_top28_i():
    r = api.search_image(random_tag(), order=Order.TOP28)
    assert r

def test_order_new_i():
    r = api.search_image(random_tag(), order=Order.NEW)
    assert r

def test_order_latest_i():
    r = api.search_image(random_tag(), order=Order.LATEST)
    assert r

def test_order_oldest_i():
    r = api.search_image(random_tag(), order=Order.OLDEST)
    assert r
