import os

from boaviztapi.utils.config import config

data_dir_test = os.path.join(os.path.dirname(__file__), "..", "tests", "data")
data_dir_prod = os.path.join(os.path.dirname(__file__), "data")

# Test data is opt-in via an env var set by BoaviztAPI's own test harness (tests/conftest.py)
if os.environ.get("BOAVIZTAPI_USE_TEST_DATA") == "1" and os.path.isdir(data_dir_test):
    data_dir = data_dir_test
else:
    data_dir = data_dir_prod

__all__ = ["config", "data_dir", "data_dir_test", "data_dir_prod"]
