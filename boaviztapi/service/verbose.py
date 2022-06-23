import json

import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component


def verbose_device(device: Device):
    json_output = {}
    for component in device.components:
        json_output[component.NAME] = verbose_component(component)

    json_output["USAGE"] = verbose_usage(device)

    return json_output


def verbose_usage(device: Device):
    json_output = {}

    for attr, val in device.usage.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if val.status != Status.NONE:
            json_output[attr[1:]] = val

    json_output["impacts"] = {
        "gwp": {
            "value": rd.round_to_sigfig(*device.impact_use_gwp()),
            "unit": "kgCO2eq"
        },
        "pe": {
            "value": rd.round_to_sigfig(*device.impact_use_pe()),
            "unit": "MJ"},
        "adp": {
            "value": rd.round_to_sigfig(*device.impact_use_adp()),
            "unit": "kgSbeq"
        },
    }
    return json_output


def verbose_component(component: Component):
    json_output = {"units": component.units}

    for attr, val in component.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if val.status != Status.NONE:
            json_output[attr.rsplit('__', 1)[1]] = val

    json_output["impacts"] = {
        "gwp": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_gwp())*component.units,
            "unit": "kgCO2eq"
        },
        "pe": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_pe())*component.units,
            "unit": "MJ"},
        "adp": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_adp())*component.units,
            "unit": "kgSbeq"
        },
    }
    return json_output
