import os
from typing import Optional

import pandas as pd

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.model.component import ComponentCPU
from boaviztapi.service.archetype import get_component_archetype


class CPU(ComponentDTO):
    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    manufacturer: Optional[str] = None
    model_range: Optional[str] = None
    family: Optional[str] = None
    name: Optional[str] = None
    tdp: Optional[int] = None

def mapper_cpu(cpu_dto: CPU, archetype=get_component_archetype(config["default_cpu"], "cpu")) -> ComponentCPU:
    cpu_component = ComponentCPU(archetype=archetype)
    cpu_component.usage = mapper_usage(cpu_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if cpu_dto.units is not None:
        cpu_component.units.set_input(cpu_dto.units)

    if cpu_dto.family is not None:
        cpu_component.family.set_input(cpu_dto.family)

    if cpu_dto.name is not None:
        cpu_component.name.set_input(cpu_dto.name)

    if cpu_dto.core_units is not None:
        cpu_component.core_units.set_input(cpu_dto.core_units)

    if cpu_dto.tdp is not None:
        cpu_component.tdp.set_input(cpu_dto.tdp)

    if cpu_dto.model_range is not None:
        cpu_component.model_range.set_input(cpu_dto.model_range)

    if cpu_dto.die_size_per_core is not None:
        cpu_component.die_size_per_core.set_input(cpu_dto.die_size_per_core)

    elif cpu_dto.die_size is not None and cpu_dto.core_units is not None:
        die_size_per_core = cpu_dto.die_size / cpu_dto.core_units
        cpu_component.die_size_per_core.set_completed(
            die_size_per_core,
            source="INPUT : die_size / core_units",
            min=die_size_per_core,
            max=die_size_per_core
        )

    return cpu_component
