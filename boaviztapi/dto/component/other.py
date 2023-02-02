from typing import Optional

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


def mapper_power_supply(power_supply_dto: PowerSupply) -> ComponentPowerSupply:
    power_supply_component = ComponentPowerSupply()

    power_supply_component.usage = smart_mapper_usage(power_supply_dto.usage or Usage())

    if power_supply_dto.units is not None:
        power_supply_component.units.value = power_supply_dto.units
        power_supply_component.units.status = Status.INPUT

    if power_supply_dto.unit_weight is not None:
        power_supply_component.unit_weight.value = power_supply_dto.unit_weight
        power_supply_component.unit_weight.status = Status.INPUT

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
        case_component.units.value = case_dto.units
        case_component.units.status = Status.INPUT

    if case_dto.case_type is not None:
        case_component.case_type.value = case_dto.case_type
        case_component.case_type.status = Status.INPUT

    case_component.usage = smart_mapper_usage(case_dto.usage or Usage())

    return case_component
