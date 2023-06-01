import pytest
import redgifs

@pytest.mark.parametrize(
    'query',
    [
        'hitomi',
        'angela white',
        'boobs',
        'ass'
    ]
)
def test_images_exist_in_result(query):
    api = redgifs.API()
    api.login()
    result = api.search_image(query)
    assert result.images
