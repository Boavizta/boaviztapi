import os
import sys
from pathlib import Path

import yaml

__version__ = '0.2.2'

if "pytest" in sys.modules:
    config_file = os.path.join(os.path.dirname(__file__), '../tests/data/test_config.yml')
else:
    config_file = os.path.join(os.path.dirname(__file__), 'data/config.yml')

config = yaml.safe_load(Path(config_file).read_text())
