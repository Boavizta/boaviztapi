import os
from pathlib import Path
import yaml

__version__ = '0.2.2'

config_file = os.path.join(os.path.dirname(__file__), 'data/config.yml')
config = yaml.safe_load(Path(config_file).read_text())