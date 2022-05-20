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


def bottom_up_component(component: Component, units: int = 1, impact_codes: Optional[Set[str]] = None) -> dict:
    component.smart_complete_data()
    gwp = component.impact_manufacture_gwp()
    pe = component.impact_manufacture_pe()
    adp = component.impact_manufacture_adp()

    impacts = {
        'gwp': {
            'manufacture': rd.round_to_sigfig(gwp[0]*units, gwp[1]),
            'use': "not implemented",
            'unit': "kgCO2eq"

        },
        'pe': {
            'manufacture': rd.round_to_sigfig(pe[0]*units, pe[1]),
            'use': "not implemented",
            'unit': "MJ"
        },
        'adp': {
            'manufacture': rd.round_to_sigfig(adp[0]*units, adp[1]),
            'use': "not implemented",
            'unit': "kgSbeq"
        },
    }
    return impacts
