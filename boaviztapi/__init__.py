import os
from pathlib import Path
from .parameters import settings
import yaml
data_dir = settings.boavizta_api_data_dir
config_file = os.path.join(settings.boavizta_api_data_dir, 'config.yml')
config = yaml.safe_load(Path(config_file).read_text())