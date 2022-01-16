from typing import Set, Optional, List

from boaviztapi.model.components.component import Component
from boaviztapi.model.devices.device import Device

_default_impacts_code = {"gwp", "pe", "adp"}


def bottom_up_device(device: Device, impact_codes: Optional[Set[str]] = None) -> dict:
    # Smart complete data
    device.smart_complete_data()

    impacts = {
        'gwp': {
            'manufacture': round(device.impact_manufacture_gwp(), 0),
            'use': round(device.impact_use_gwp(), 0)
        },
        'pe': {
            'manufacture': round(device.impact_manufacture_pe(), 0),
            'use': "Not Implemented"
        },
        'adp': {
            'manufacture': round(device.impact_manufacture_adp(), 3),
            'use': "Not Implemented"
        },
    }
    return impacts


def bottom_up_component(component: Component, impact_codes: Optional[Set[str]] = None) -> dict:
    component.smart_complete_data()
    impacts = {
        'gwp': {
            'manufacture': round(component.impact_gwp(), 0),
            'use': "not implemented"
        },
        'pe': {
            'manufacture': round(component.impact_pe(), 0),
            'use': "not implemented"
        },
        'adp': {
            'manufacture': round(component.impact_adp(), 3),
            'use': "not implemented"
        },
    }
    return impacts
