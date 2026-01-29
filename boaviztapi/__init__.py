import os
import sys

from boaviztapi.utils.config import config

data_dir_test = os.path.join(os.path.dirname(__file__), "..", "tests", "data")
data_dir_prod = os.path.join(os.path.dirname(__file__), "data")

# Use test data if using pytest, and not running E2E tests
if "pytest" in sys.modules and "--rune2e" not in sys.argv:
    data_dir = data_dir_test
else:
    data_dir = data_dir_prod

__all__ = ["config", "data_dir", "data_dir_test", "data_dir_prod"]
