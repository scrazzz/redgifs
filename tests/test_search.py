import pytest

from redgifs import API

api = API()
api.login()

@pytest.mark.parametrize(
    "search_text, searched_for",
    [
        ('african', 'African'),
        ('ahegao', 'Ahegao'),
        ('ana lord', 'Ana Lorde'),
        ('sex', 'Sex'),
    ]
)
def test_search_with_search_text(search_text, searched_for):
    result = api.search(search_text)
    assert result.searched_for == searched_for


@pytest.mark.parametrize(
    "count, expected_count",
    # [ (10, 10), (20, 20), (35, 35) ]
    [ (10, 10), (20, 20), (28, 28) ]
)
def test_search_with_count(count, expected_count):
    result = api.search('hitomi tanaka', count=count)
    assert result.gifs is not None and len(result.gifs) == expected_count


@pytest.mark.parametrize(
    "page, expected_page",
    [ (2, 2), (3, 3), (6, 6) ]
)
def test_search_with_page(page, expected_page):
    result = api.search('big dick', page=page)
    assert result.page == expected_page
