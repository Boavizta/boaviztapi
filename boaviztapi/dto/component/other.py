from typing import Optional

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.model.component import ComponentPowerSupply, ComponentMotherboard, ComponentCase
from boaviztapi.service.archetype import get_component_archetype


class PowerSupply(ComponentDTO):
    unit_weight: Optional[float] = None


class Motherboard(ComponentDTO):
    pass


class Case(ComponentDTO):
    case_type: str = None


def mapper_power_supply(power_supply_dto: PowerSupply, archetype=get_component_archetype(config["default_power_supply"],
                                                                                         "power_supply")) -> ComponentPowerSupply:
    power_supply_component = ComponentPowerSupply(archetype=archetype)
    power_supply_component.usage = mapper_usage(power_supply_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if power_supply_dto.units is not None:
        power_supply_component.units.set_input(power_supply_dto.units)

    if power_supply_dto.unit_weight is not None:
        power_supply_component.unit_weight.set_input(power_supply_dto.unit_weight)

    return power_supply_component


def mapper_motherboard(motherboard_dto: Motherboard) -> ComponentMotherboard:
    motherboard_component = ComponentMotherboard()
    motherboard_component.usage = mapper_usage(motherboard_dto.usage or Usage())

    if motherboard_dto.units is not None:
        motherboard_component.units.set_input(motherboard_dto.units)

    return motherboard_component


def mapper_case(case_dto: Case, archetype=get_component_archetype(config["default_case"], "case")) -> ComponentCase:
    case_component = ComponentCase(archetype=archetype)
    case_component.usage = mapper_usage(case_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if case_dto.units is not None:
        case_component.units.set_input(case_dto.units)

    if case_dto.case_type is not None:
        case_component.case_type.set_input(case_dto.case_type)

    return case_component


class FunctionalBlock(ComponentDTO):
    hsl_level: str = None
    type: str = None
