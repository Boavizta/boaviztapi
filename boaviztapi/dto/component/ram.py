import os
from typing import Optional

import pandas as pd

from boaviztapi import config
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


def smart_mapper_ram(ram_dto: RAM, default_config=config["DEFAULT"]["RAM"]) -> ComponentRAM:
    ram_component = ComponentRAM(default_config=default_config)

    if ram_dto.units is not None:
        ram_component.units.set_input(ram_dto.units)

    ram_component.usage = smart_mapper_usage(ram_dto.usage or Usage())

    corrected_manufacturer = None

    if ram_dto.density is not None:
        ram_component.density.set_input(ram_dto.density)
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
            ram_component.density.set_completed(
                float(sub['density']),
                source=str(sub['manufacturer'].iloc[0]),
                min=float(sub['density']),
                max=float(sub['density'])
            )
        else:
            ram_component.density.set_completed(
                float(sub['density'].mean()),
                source="Average of " + str(len(sub)) + " rows",
                min=float(sub['density'].min()),
                max=float(sub['density'].max())
            )

    if ram_dto.capacity is not None:
        ram_component.capacity.set_input(ram_dto.capacity)

    if ram_dto.manufacturer is not None and corrected_manufacturer is not None:
        if ram_dto.manufacturer != corrected_manufacturer:
            ram_component.manufacturer.set_changed(corrected_manufacturer)
        else:
            ram_component.manufacturer.set_input(ram_dto.manufacturer)

    if ram_dto.process is not None:
        ram_component.process.set_input(ram_dto.process)

    return ram_component

