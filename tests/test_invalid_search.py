import pytest

from redgifs import API

@pytest.mark.xfail
def test_invalid():
    api = API()
    api.search('abcd')
