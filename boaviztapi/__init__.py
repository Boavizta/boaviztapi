import os
import sys

from boaviztapi.utils.config import config

# Use test data directory when running under pytest
if "pytest" in sys.modules:
    data_dir = os.path.join(os.path.dirname(__file__), "..", "tests", "data")
else:
    data_dir = os.path.join(os.path.dirname(__file__), "data")

__all__ = ["config", "data_dir"]
