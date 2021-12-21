from typing import Set, Optional, List

from api.model.components.component import Component
from api.model.devices.device import Device

_default_impacts_code = {"gwp", "pe", "adp"}


def bottom_up_device(device: Device, impact_codes: Optional[Set[str]] = None) -> dict:
    # Smart complete data
    device.smart_complete_data()

    impacts = {
        'gwp': round(device.impact_gwp(), 0),
        'pe': round(device.impact_pe(), 0),
        'adp': round(device.impact_adp(), 3)
    }
    return impacts


def bottom_up_component(component: Component, impact_codes: Optional[Set[str]] = None) -> dict:
    component.smart_complete_data()
    impacts = {
        'gwp': round(component.impact_gwp(), 0),
        'pe': round(component.impact_pe(), 0),
        'adp': round(component.impact_adp(), 3)
    }
    return impacts
