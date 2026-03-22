"""
Pytest configuration for the test suite.

This file defines an autouse fixture that adds a one-second delay before
running tests that perform real API calls to Redgifs. This helps avoid
hitting rate limits during the online tests without affecting offline ones.
"""

import time
import pytest

# List of files which really use online API (and can be rate-limited)
ONLINE_TEST_FILES = {
    "test_gif_creator_attrs.py",
    "test_images_attrs.py",
    "test_order.py",
    "test_routes.py",
}

@pytest.fixture(autouse=True)
def slow_down_for_online_tests(request):
    """
    Adds a short delay before running tests that perform real API calls.

    This helps avoid hitting Redgifs rate limits during the test suite.
    """
    test_file = request.fspath.basename
    if test_file in ONLINE_TEST_FILES:
        time.sleep(1)
