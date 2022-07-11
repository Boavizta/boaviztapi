import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component


def verbose_device(device: Device):
    json_output = {}
    for component in device.components:
        if f"{component.NAME}-1" in json_output:
            i = 2
            while f"{component.NAME}-{i}" in json_output:
                i += 1
            key = f"{component.NAME}-{i}"
        else:
            key = f"{component.NAME}-1"

        json_output[key] = verbose_component(component)

    json_output["USAGE"] = verbose_usage(device)

    return json_output


def verbose_usage(device: Device):
    json_output = {}

    for attr, val in device.usage.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if val.status != Status.NONE:
            json_output[attr] = val.to_json()

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

    json_output["impacts"] = {
        "gwp": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_gwp()) * component.units,
            "unit": "kgCO2eq"
        },
        "pe": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_pe()) * component.units,
            "unit": "MJ"},
        "adp": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_adp()) * component.units,
            "unit": "kgSbeq"
        },
    }
    for attr, val in component.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if val.status != Status.NONE:
            json_output[attr] = val.to_json()

    return json_output
