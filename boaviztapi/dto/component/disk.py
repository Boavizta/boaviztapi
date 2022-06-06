from typing import Optional

import pandas as pd

from boaviztapi.dto.component import ComponentDTO


_ssd_df = pd.read_csv('./boaviztapi/data/components/ssd_manufacture.csv')


class Disk(ComponentDTO):
    type: Optional[str] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None


def smart_complete_disk_ssd(disk: Disk) -> Disk:
    disk_ = disk.copy()
    if disk.type.lower() == 'ssd':
        sub = _ssd_df

        if disk_.manufacturer is not None:
            sub = sub[sub['manufacturer'] == disk_.manufacturer]

        if len(sub) == 0 or len(sub) == len(_ssd_df):
            pass
        elif len(sub) == 1:
            disk_.density = float(sub['density'])
        else:
            if disk_.capacity is not None:
                capacity = disk_.capacity
                sub['_scope3'] = sub['density'].apply(lambda x: capacity / x)
                sub = sub.sort_values(by='_scope3', ascending=False)
                density = float(sub.iloc[0].density)
                disk_.density = density
    return disk_
