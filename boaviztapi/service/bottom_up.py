from typing import Union, Optional

from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
import boaviztapi.utils.roundit as rd
from boaviztapi.service.allocation import allocate, Allocation

NOT_IMPLEMENTED = 'not implemented'


def bottom_up_component(component: Component, allocation: Allocation) -> dict:
    impacts = {
        'gwp': {
            'manufacture': get_model_impact(component, 'manufacture', 'gwp', component.units, allocation) or NOT_IMPLEMENTED,
            'use': get_model_impact(component, 'use', 'gwp', component.units) or NOT_IMPLEMENTED,
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': get_model_impact(component, 'manufacture', 'pe', component.units, allocation) or NOT_IMPLEMENTED,
            'use': get_model_impact(component, 'use', 'pe', component.units) or NOT_IMPLEMENTED,
            'unit': "MJ"
        },
        'adp': {
            'manufacture': get_model_impact(component, 'manufacture', 'adp', component.units, allocation) or NOT_IMPLEMENTED,
            'use': get_model_impact(component, 'use', 'adp', component.units) or NOT_IMPLEMENTED,
            'unit': "kgSbeq"
        },
    }
    return impacts


def get_model_impact(model: Union[Component, Device],
                     phase: str,
                     impact_type: str,
                     units: int = 1,
                     allocation_type: Allocation = Allocation.TOTAL) -> Optional[float]:
    try:
        impact_function = model.__getattribute__(f'impact_{phase}_{impact_type}')
        impact, significant_figures = impact_function()

        if phase == "manufacture":
            impact = allocate(impact, allocation_type, model.usage)

        units_impact = impact * units
        return rd.round_to_sigfig(units_impact, significant_figures)
    except (AttributeError, NotImplementedError):
        pass


def bottom_up_device(device: Device, allocation) -> dict:
    impacts = {
        'gwp': {
            'manufacture': get_model_impact(device, 'manufacture', 'gwp', allocation_type=allocation) or NOT_IMPLEMENTED,
            'use': get_model_impact(device, 'use', 'gwp') or NOT_IMPLEMENTED,
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': get_model_impact(device, 'manufacture', 'pe', allocation_type=allocation) or NOT_IMPLEMENTED,
            'use': get_model_impact(device, 'use', 'pe') or NOT_IMPLEMENTED,
            'unit': "MJ"
        },
        'adp': {
            'manufacture': get_model_impact(device, 'manufacture', 'adp', allocation_type=allocation) or NOT_IMPLEMENTED,
            'use': get_model_impact(device, 'use', 'adp') or NOT_IMPLEMENTED,
            'unit': "kgSbeq"
        },
    }
    return impacts
