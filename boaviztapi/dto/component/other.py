from typing import Optional

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import smart_mapper_usage, Usage
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentPowerSupply, ComponentMotherboard, ComponentCase


class PowerSupply(ComponentDTO):
    unit_weight: Optional[float] = None


class Motherboard(ComponentDTO):
    pass


class Case(ComponentDTO):
    case_type: str = None


def mapper_power_supply(power_supply_dto: PowerSupply, default_config=config['DEFAULT']['POWER_SUPPLY']) -> ComponentPowerSupply:
    power_supply_component = ComponentPowerSupply(default_config=default_config)

    power_supply_component.usage = smart_mapper_usage(power_supply_dto.usage or Usage())

    if power_supply_dto.units is not None:
        power_supply_component.units.set_input(power_supply_dto.units)

    if power_supply_dto.unit_weight is not None:
        power_supply_component.unit_weight.set_input(power_supply_dto.unit_weight)

    return power_supply_component


def mapper_motherboard(motherboard_dto: Motherboard) -> ComponentMotherboard:
    motherboard_component = ComponentMotherboard()

    motherboard_component.usage = smart_mapper_usage(motherboard_dto.usage or Usage())

    if motherboard_dto.units is not None:
        motherboard_component.units.value = motherboard_dto.units
        motherboard_component.units.status = Status.INPUT

    return motherboard_component


def mapper_case(case_dto: Case) -> ComponentCase:
    case_component = ComponentCase()

    if case_dto.units is not None:
        case_component.units.set_input(case_dto.units)

    if case_dto.case_type is not None:
        case_component.case_type.set_input(case_dto.case_type)

    case_component.usage = smart_mapper_usage(case_dto.usage or Usage())

    return case_component
