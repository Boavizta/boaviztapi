import os
from typing import Optional

import pandas as pd

from boaviztapi.dto.component import ComponentDTO
import os

_cpu_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/components/cpu_manufacture.csv'))


class CPU(ComponentDTO):
    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    manufacturer: Optional[str] = None
    model_range: Optional[str] = None
    family: Optional[str] = None
    name: Optional[str] = None


def smart_complete_cpu(cpu: CPU) -> CPU:
    cpu_ = cpu.copy()
    if cpu_.die_size_per_core is None and cpu_.die_size is None:
        sub = _cpu_df

        if cpu_.family is not None:
            tmp = sub[sub['family'] == cpu_.family]
            if len(tmp) > 0:
                sub = tmp.copy()

        if cpu_.core_units is not None:
            tmp = sub[sub['core_units'] == cpu_.core_units]
            if len(tmp) > 0:
                sub = tmp.copy()

        if len(sub) == 0 or len(sub) == len(_cpu_df):
            pass
        elif len(sub) == 1:
            cpu_.die_size_per_core = float(sub['die_size_per_core'])
        else:
            sub['_scope3'] = sub[['core_units', 'die_size_per_core']].apply(lambda x: x[0] * x[1], axis=1)
            sub = sub.sort_values(by='_scope3', ascending=False)
            row = sub.iloc[0]
            cpu_.die_size_per_core = float(row['die_size_per_core'])
            cpu_.core_units = int(row['core_units'])
    return cpu_
