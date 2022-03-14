from typing import Set, Optional

from boaviztapi.model.components.component import Component
from boaviztapi.model.devices.device import Device
import boaviztapi.utils.roundit as rd

_default_impacts_code = {"gwp", "pe", "adp"}


def bottom_up_device(device: Device, impact_codes: Optional[Set[str]] = None) -> dict:
    # Smart complete data
    device.smart_complete_data()

    impacts = {
        'gwp': {
            'manufacture': rd.round_to_sigfig(*device.impact_manufacture_gwp()),
            'use': rd.round_to_sigfig(*device.impact_use_gwp()),
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': rd.round_to_sigfig(*device.impact_manufacture_pe()),
            'use': "Not Implemented",
            'unit': "MJ"
        },
        'adp': {
            'manufacture': rd.round_to_sigfig(*device.impact_manufacture_adp()),
            'use': "Not Implemented",
            'unit': "kgSbeq"
        },
    }
    return impacts


def bottom_up_component(component: Component, impact_codes: Optional[Set[str]] = None) -> dict:
    component.smart_complete_data()
    impacts = {
        'gwp': {
            'manufacture': rd.round_to_sigfig(*component.impact_gwp()),
            'use': "not implemented",
            'unit': "kgCO2eq"

        },
        'pe': {
            'manufacture': rd.round_to_sigfig(*component.impact_pe()),
            'use': "not implemented",
            'unit': "MJ"
        },
        'adp': {
            'manufacture': rd.round_to_sigfig(*component.impact_adp()),
            'use': "not implemented",
            'unit': "kgSbeq"
        },
    }
    return impacts
