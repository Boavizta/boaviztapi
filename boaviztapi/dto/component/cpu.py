import os
from typing import Optional

import pandas as pd

from boaviztapi.dto.component import ComponentDTO
import os

from boaviztapi.dto.usage.usage import smart_mapper_usage, Usage
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentCPU

_cpu_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/components/cpu_manufacture.csv'))


class CPU(ComponentDTO):
    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    manufacturer: Optional[str] = None
    model_range: Optional[str] = None
    family: Optional[str] = None
    name: Optional[str] = None


def smart_mapper_cpu(cpu_dto: CPU) -> ComponentCPU:
    cpu_component = ComponentCPU()
    cpu_component.usage = smart_mapper_usage(cpu_dto.usage or Usage())

    cpu_component.units = cpu_dto.units

    if cpu_dto.die_size_per_core is not None:
        cpu_component.die_size_per_core.value = cpu_dto.die_size_per_core
        cpu_component.die_size_per_core.status = Status.INPUT

    elif cpu_dto.die_size is not None and cpu_dto.core_units is not None:
        cpu_component.die_size_per_core.value = cpu_dto.die_size / cpu_dto.core_units
        cpu_component.die_size_per_core.status = Status.COMPLETED
        cpu_component.die_size_per_core.source = "INPUT : die_size / core_units"

    else:
        sub = _cpu_df
        if cpu_dto.family is not None:

            tmp = sub[sub['family'] == cpu_dto.family]
            if len(tmp) > 0:
                cpu_component.family.value = cpu_dto.family
                cpu_component.family.status = Status.INPUT
                sub = tmp.copy()

        if cpu_dto.core_units is not None:
            tmp = sub[sub['core_units'] == cpu_dto.core_units]
            if len(tmp) > 0:
                cpu_component.core_units.value = cpu_dto.core_units
                cpu_component.core_units.status = Status.INPUT
                sub = tmp.copy()

        if len(sub) == 0 or len(sub) == len(_cpu_df):
            pass
        elif len(sub) == 1:
            cpu_component.die_size_per_core.value = float(sub['die_size_per_core'])
            cpu_component.die_size_per_core.status = Status.COMPLETED
            cpu_component.die_size_per_core.source = sub['Source']
        else:
            sub['_scope3'] = sub[['core_units', 'die_size_per_core']].apply(lambda x: x[0] * x[1], axis=1)
            sub = sub.sort_values(by='_scope3', ascending=False)
            row = sub.iloc[0]

            cpu_component.die_size_per_core.value = float(row['die_size_per_core'])
            if cpu_dto.die_size_per_core != cpu_component.die_size_per_core.value:
                cpu_component.die_size_per_core.status = Status.CHANGED
            else:
                cpu_component.die_size_per_core.status = Status.COMPLETED
            cpu_component.die_size_per_core.source = row['Source']

            if cpu_dto.die_size_per_core != cpu_component.die_size_per_core.value:
                cpu_component.core_units.status = Status.CHANGED
            else:
                cpu_component.core_units.status = Status.COMPLETED
            cpu_component.core_units.value = int(row['core_units'])
            cpu_component.core_units.source = row['Source']
    return cpu_component
