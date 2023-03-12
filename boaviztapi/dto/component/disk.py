import os
from typing import Optional

import pandas as pd

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentSSD, ComponentHDD
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf



class Disk(ComponentDTO):
    type: Optional[str] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None


def mapper_ssd(disk_dto: Disk, default_config=config['DEFAULT']['SSD']) -> ComponentSSD:
    disk_component = ComponentSSD(default_config=default_config)
    disk_component.usage = mapper_usage(disk_dto.usage or Usage())

    if disk_dto.units is not None:
        disk_component.units.set_input(disk_dto.units)

    if disk_dto.capacity is not None:
        disk_component.capacity.set_input(disk_dto.capacity)

    if disk_dto.density is not None:
        disk_component.density.set_input(disk_dto.density)

    return disk_component


def mapper_hdd(disk_dto: Disk, default_config=config['DEFAULT']['HDD']) -> ComponentHDD:
    disk_component = ComponentHDD(default_config=default_config)
    disk_component.usage = mapper_usage(disk_dto.usage or Usage())

    if disk_dto.units is not None:
        disk_component.units.set_input(disk_dto.units)
    if disk_dto.capacity is not None:
        disk_component.capacity.set_input(disk_dto.capacity)

    return disk_component
