from typing import Set, Optional

from boaviztapi.model.components.component import Component
from boaviztapi.model.devices.device import Device
import boaviztapi.utils.roundit as rd

_default_impacts_code = {"gwp", "pe", "adp"}


def bottom_up_device(device: Device, impact_codes: Optional[Set[str]] = None) -> dict:

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
    gwp_manuf = component.impact_manufacture_gwp()
    pe_manuf = component.impact_manufacture_pe()
    adp_manuf = component.impact_manufacture_adp()

    gwp_use = component.impact_use_gwp()
    pe_use = component.impact_use_pe()
    adp_use = component.impact_use_adp()

    impacts = {
        'gwp': {
            'manufacture': rd.round_to_sigfig(gwp_manuf[0]*units, gwp_manuf[1]),
            'use': gwp_use if gwp_use == "not implemented" else rd.round_to_sigfig(gwp_use[0]*units, gwp_use[1]),
            'unit': "kgCO2eq"
        },
        'pe': {
            'manufacture': rd.round_to_sigfig(pe_manuf[0]*units, pe_manuf[1]),
            'use': pe_use if pe_use == "not implemented" else rd.round_to_sigfig(pe_use[0]*units, pe_use[1]),
            'unit': "MJ"
        },
        'adp': {
            'manufacture': rd.round_to_sigfig(adp_manuf[0]*units, adp_manuf[1]),
            'use': adp_use if adp_use == "not implemented" else rd.round_to_sigfig(adp_use[0]*units, adp_use[1]),
            'unit': "kgSbeq"
        },
    }
    return impacts