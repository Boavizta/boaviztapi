from typing import Union, Tuple, Optional

from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
import boaviztapi.utils.roundit as rd


NOT_IMPLEMENTED = 'not implemented'


def bottom_up_device(device: Device) -> dict:
    impacts = {
        'gwp': {
            'manufacture': rd.round_to_sigfig(*device.impact_manufacture_gwp()),
            'use': rd.round_to_sigfig(*device.impact_use_gwp()),
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': rd.round_to_sigfig(*device.impact_manufacture_pe()),
            'use': rd.round_to_sigfig(*device.impact_use_pe()),
            'unit': "MJ"
        },
        'adp': {
            'manufacture': rd.round_to_sigfig(*device.impact_manufacture_adp()),
            'use': rd.round_to_sigfig(*device.impact_use_adp()),
            'unit': "kgSbeq"
        },
    }
    return impacts


def bottom_up_component(component: Component, units: int = 1) -> dict:
    impacts = {
        'gwp': {
            'manufacture': get_component_impact(component, 'manufacture', 'gwp', units) or NOT_IMPLEMENTED,
            'use': get_component_impact(component, 'use', 'pe', units) or NOT_IMPLEMENTED,
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': get_component_impact(component, 'manufacture', 'pe', units) or NOT_IMPLEMENTED,
            'use': get_component_impact(component, 'use', 'pe', units) or NOT_IMPLEMENTED,
            'unit': "MJ"
        },
        'adp': {
            'manufacture': get_component_impact(component, 'manufacture', 'adp', units) or NOT_IMPLEMENTED,
            'use': get_component_impact(component, 'use', 'adp', units) or NOT_IMPLEMENTED,
            'unit': "kgSbeq"
        },
    }
    return impacts


def get_component_impact(component: Component,
                         phase: str,
                         impact_type: str,
                         units: int) -> Optional[float]:
    try:
        impact_function = component.__getattribute__(f'impact_{phase}_{impact_type}')
        impact, significant_figures = impact_function()
        units_impact = impact * units
        return rd.round_to_sigfig(units_impact, significant_figures)
    except (AttributeError, NotImplementedError):
        pass
