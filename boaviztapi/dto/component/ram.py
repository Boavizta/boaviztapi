import os
from typing import Optional

import pandas as pd

from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage import Usage
from boaviztapi.dto.usage.usage import smart_mapper_usage
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentRAM
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf

_ram_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/components/ram_manufacture.csv'))


class RAM(ComponentDTO):
    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None


def smart_mapper_ram(ram_dto: RAM) -> ComponentRAM:
    ram_component = ComponentRAM()

    ram_component.units = ram_dto.units

    ram_component.usage = smart_mapper_usage(ram_dto.usage or Usage())

    corrected_manufacturer = None

    if ram_dto.density is not None:
        ram_component.density.value = ram_dto.density
        ram_component.density.status = Status.INPUT
    else:
        sub = _ram_df

        if ram_dto.manufacturer is not None:
            corrected_manufacturer = fuzzymatch_attr_from_pdf(ram_dto.manufacturer, "manufacturer", sub)
            sub = sub[sub['manufacturer'] == corrected_manufacturer]

        if ram_dto.process is not None:
            sub = sub[sub['process'] == ram_dto.process]

        if len(sub) == 0 or len(sub) == len(_ram_df):
            pass
        elif len(sub) == 1:
            ram_component.density.value = float(sub['density'])
            ram_component.density.status = Status.COMPLETED
            ram_component.density.source = sub['manufacturer']
        else:
            sub['_scope3'] = sub['density'].apply(lambda x: x)
            sub = sub.sort_values(by='_scope3', ascending=True)
            row = sub.iloc[0]

            ram_component.density.value = float(row['density'])
            ram_component.density.status = Status.COMPLETED
            ram_component.density.source = row['manufacturer']

    if ram_dto.capacity is not None:
        ram_component.capacity.value = ram_dto.capacity
        ram_component.capacity.status = Status.INPUT

    if ram_dto.manufacturer is not None and corrected_manufacturer is not None:
        if ram_dto.manufacturer != corrected_manufacturer:
            ram_component.manufacturer.value = corrected_manufacturer
            ram_component.manufacturer.status = Status.CHANGED
        else:
            ram_component.manufacturer.value = ram_dto.manufacturer
            ram_component.manufacturer.status = Status.INPUT

    if ram_dto.process is not None:
        ram_component.process.value = ram_dto.process
        ram_component.process.status = Status.INPUT

    return ram_component

