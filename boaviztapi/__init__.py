import os
import sys
from pathlib import Path

import yaml

__version__ = '1.0.0-alpha'

if "pytest" in sys.modules:
    data_dir = os.path.join(os.path.dirname(__file__), '../tests/data')
else:
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

config_file = os.path.join(data_dir, 'config.yml')
config = yaml.safe_load(Path(config_file).read_text())
