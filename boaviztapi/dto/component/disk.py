from typing import Optional


from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.model.component import ComponentSSD, ComponentHDD
from boaviztapi.service.archetype import get_component_archetype


class Disk(ComponentDTO):
    type: Optional[str] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    layers: Optional[int] = None


def mapper_ssd(disk_dto: Disk, archetype=get_component_archetype(config["default_ssd"], "ssd")) -> ComponentSSD:
    disk_component = ComponentSSD(archetype=archetype)
    disk_component.usage = mapper_usage(disk_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if disk_dto.units is not None:
        disk_component.units.set_input(disk_dto.units)

    if disk_dto.capacity is not None:
        disk_component.capacity.set_input(disk_dto.capacity)

    if disk_dto.manufacturer is not None:
        disk_component.manufacturer.set_input(disk_dto.manufacturer)

    if disk_dto.density is not None:
        disk_component.density.set_input(disk_dto.density)

    if disk_dto.layers is not None:
        disk_component.layers.set_input(disk_dto.layers)

    return disk_component


def mapper_hdd(disk_dto: Disk, archetype=get_component_archetype(config["default_hdd"], "hdd")) -> ComponentHDD:
    disk_component = ComponentHDD(archetype=archetype)
    disk_component.usage = mapper_usage(disk_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if disk_dto.units is not None:
        disk_component.units.set_input(disk_dto.units)
    if disk_dto.capacity is not None:
        disk_component.capacity.set_input(disk_dto.capacity)

    return disk_component
