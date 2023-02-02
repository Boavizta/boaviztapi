from typing import Union, Optional

from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
from boaviztapi.model.impact import Impact, IMPACT_CRITERIAS, IMPACT_PHASES
from boaviztapi.service.allocation import allocate, Allocation

NOT_IMPLEMENTED = 'not implemented'


def bottom_up_component(component: Component, allocation: Allocation) -> dict:
    impacts = {
        'gwp': {
            'manufacture': get_model_single_impact(component, 'manufacture', 'gwp', allocation) or NOT_IMPLEMENTED,
            'use': get_model_single_impact(component, 'use', 'gwp', component.units) or NOT_IMPLEMENTED,
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': get_model_single_impact(component, 'manufacture', 'pe', allocation) or NOT_IMPLEMENTED,
            'use': get_model_single_impact(component, 'use', 'pe', component.units) or NOT_IMPLEMENTED,
            'unit': "MJ"
        },
        'adp': {
            'manufacture': get_model_single_impact(component, 'manufacture', 'adp', allocation) or NOT_IMPLEMENTED,
            'use': get_model_single_impact(component, 'use', 'adp', component.units) or NOT_IMPLEMENTED,
            'unit': "kgSbeq"
        },
    }
    return impacts


def get_model_single_impact(model: Union[Component, Device],
                            phase: str,
                            impact_type: str,
                            allocation_type: Allocation = Allocation.TOTAL) -> Optional[Impact]:
        impact_function = model.__getattribute__(f'impact_{phase}_{impact_type}')
        impact, significant_figures, min_impact, max_impact, warnings = impact_function()

        if phase == "manufacture":
            impact = allocate(impact, allocation_type, model.usage)

        return Impact(
            value=impact*model.units.value,
            significant_figures=significant_figures,
            min=min_impact*model.units.min,
            max=max_impact*model.units.max,
            warnings=warnings
        )

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
