import os
from typing import Optional

import pandas as pd

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage import Usage
from boaviztapi.dto.usage.usage import mapper_usage
from boaviztapi.model.component import ComponentRAM
from boaviztapi.service.archetype import get_component_archetype

_ram_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/crowdsourcing/ram_manufacture.csv'))


class RAM(ComponentDTO):
    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None


def mapper_ram(ram_dto: RAM, archetype=get_component_archetype(config["default_ram"], "ram")) -> ComponentRAM:
    ram_component = ComponentRAM(archetype=archetype)
    ram_component.usage = mapper_usage(ram_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if ram_dto.units is not None:
        ram_component.units.set_input(ram_dto.units)

    if ram_dto.density is not None:
        ram_component.density.set_input(ram_dto.density)

    if ram_dto.capacity is not None:
        ram_component.capacity.set_input(ram_dto.capacity)

    if ram_dto.manufacturer is not None:
        ram_component.manufacturer.set_input(ram_dto.manufacturer)

    if ram_dto.process is not None:
        ram_component.process.set_input(ram_dto.process)

    return ram_component

