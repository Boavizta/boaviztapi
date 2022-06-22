import os
from typing import Optional

import pandas as pd

from boaviztapi.dto.component import ComponentDTO


_ram_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/components/ram_manufacture.csv'))


class RAM(ComponentDTO):
    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None


def smart_complete_ram(ram: RAM) -> RAM:
    ram_ = ram.copy()
    if ram_.density is None:
        sub = _ram_df

        if ram_.manufacturer is not None:
            sub = sub[sub['manufacturer'] == ram_.manufacturer]

        if ram_.process is not None:
            sub = sub[sub['process'] == ram_.process]

        if len(sub) == 0 or len(sub) == len(_ram_df):
            pass
        elif len(sub) == 1:
            ram_.density = float(sub['density'])
        else:
            sub['_scope3'] = sub['density'].apply(lambda x: x)
            sub = sub.sort_values(by='_scope3', ascending=True)
            density = float(sub.iloc[0].density)
            ram_.density = density
    return ram_
