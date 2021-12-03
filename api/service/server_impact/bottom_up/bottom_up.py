from typing import Set, Optional, List

import pandas as pd
from pydantic import BaseModel

from api.model.impacts import Impact
from api.model.server import Server, Cpu, Ram, Disk
from .impact_factor import impact_factor

_default_impacts_code = {"gwp", "pe", "adp"}

# Data
_cpu_df = pd.read_csv('./api/model/cpu.csv')
_ram_df = pd.read_csv('./api/model/ram.csv')
_ssd_df = pd.read_csv('./api/model/ssd.csv')


# Constants
DEFAULT_CPU_UNITS = 2
DEFAULT_CPU_DIE_SIZE_PER_CORE = 0.245
DEFAULT_CPU_CORE_UNITS = 24

DEFAULT_RAM_UNITS = 2
DEFAULT_RAM_CAPACITY = 32
DEFAULT_RAM_DENSITY = 0.625

DEFAULT_SSD_UNITS = 2
DEFAULT_SSD_CAPACITY = 1000
DEFAULT_SSD_DENSITY = 48.5

DEFAULT_POWER_SUPPLY_NUMBER = 2
DEFAULT_POWER_SUPPLY_WEIGHT = 2.99


def bottom_up_components(components: List[BaseModel], impact_codes: Optional[Set[str]] = None) -> dict:
    # Smart complete data
    for item in components:
        item.smart_complete_data()

    impacts = {
        'gwp': sum([item.impact_gwp() for item in components]),
        'pe': sum([item.impact_pe() for item in components]),
        'adp': sum([item.impact_adp() for item in components])
    }
    return impacts
