from typing import Union, Optional

from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
from boaviztapi.model.impact import Impact, IMPACT_CRITERIAS, IMPACT_PHASES
from boaviztapi.service.allocation import allocate, Allocation

NOT_IMPLEMENTED = 'not implemented'


def bottom_up_component(component: Component, allocation: Allocation) -> dict:
    impacts = {
        'gwp': {
            'manufacture': get_model_single_impact(component, 'manufacture', 'gwp', component.units, allocation) or NOT_IMPLEMENTED,
            'use': get_model_single_impact(component, 'use', 'gwp', component.units) or NOT_IMPLEMENTED,
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': get_model_single_impact(component, 'manufacture', 'pe', component.units, allocation) or NOT_IMPLEMENTED,
            'use': get_model_single_impact(component, 'use', 'pe', component.units) or NOT_IMPLEMENTED,
            'unit': "MJ"
        },
        'adp': {
            'manufacture': get_model_single_impact(component, 'manufacture', 'adp', component.units, allocation) or NOT_IMPLEMENTED,
            'use': get_model_single_impact(component, 'use', 'adp', component.units) or NOT_IMPLEMENTED,
            'unit': "kgSbeq"
        },
    }
    return impacts


def get_model_single_impact(model: Union[Component, Device],
                            phase: str,
                            impact_type: str,
                            units: int = 1,
                            allocation_type: Allocation = Allocation.TOTAL) -> Optional[Impact]:
    try:
        impact_function = model.__getattribute__(f'impact_{phase}_{impact_type}')
        value, significant_figures, error_margin, warnings = impact_function()

        if phase == "manufacture":
            value = allocate(value, allocation_type, model.usage)

        units_impact = value * units
        return Impact(value=units_impact, significant_figures=significant_figures, error_margin=error_margin, warnings=warnings)

    except (AttributeError, NotImplementedError):
        pass

def bottom_up_device(device: Device, allocation) -> dict:
    impacts = {}

    for criteria in IMPACT_CRITERIAS:
        impacts[criteria.name] = {}
        for phase in IMPACT_PHASES:
            single_impact = get_model_single_impact(device, phase, criteria.name, allocation_type=allocation)
            impacts[criteria.name][phase] = single_impact.to_json() if single_impact else NOT_IMPLEMENTED
        impacts[criteria.name]["unit"] = criteria.unit
        impacts[criteria.name]["description"] = criteria.description

    return impacts
