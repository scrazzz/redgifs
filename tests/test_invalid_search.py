from redgifs import API

import pytest

@pytest.mark.xfail
def test_invalid():
    api = API()
    api.search('abcd')
