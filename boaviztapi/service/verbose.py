import json

import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component


def verbose_device(device: Device):
    json_output = {}
    # if complete_device.usage:
    #     json_output["USAGE"] = {**verbose_usage(complete_device=complete_device,
    #                                             input_device=input_device)}
    for component in device.components:
        json_output[component.NAME] = verbose_component(component)

    return json_output


def verbose_usage(complete_device, input_device):
    json_output = {"unit": 1}

    for attr, value in complete_device.usage.__iter__():
        if type(value) is dict:
            json_output[attr] = \
                recursive_dict_verbose(value,
                                       {} if getattr(input_device.usage, attr) is None else getattr(input_device.usage,
                                                                                                    attr))
        elif value is not None and attr != "TYPE" and attr != "hash":
            json_output[attr] = {}
            json_output[attr]["input_value"] = getattr(input_device.usage, attr, None)
            json_output[attr]["used_value"] = value
            json_output[attr]["status"] = get_status(json_output[attr]["used_value"], json_output[attr]["input_value"])

    gwp_use = complete_device.impact_use_gwp()
    pe_use = complete_device.impact_use_pe()
    adp_use = complete_device.impact_use_adp()

    json_output["impacts"] = {"gwp": {
        "value": gwp_use if gwp_use == "not implemented" else rd.round_to_sigfig(gwp_use[0], gwp_use[1]),
        "unit": "kgCO2eq"},
        "pe": {
            "value": pe_use if pe_use == "not implemented" else rd.round_to_sigfig(pe_use[0], pe_use[1]),
            "unit": "MJ"},
        "adp": {"value": adp_use if adp_use == "not implemented" else rd.round_to_sigfig(adp_use[0], adp_use[1]),
                "unit": "kgSbeq"},
    }
    return json_output


def verbose_component(component: Component):
    json_output = {"units": component.units}

    # TODO: Reimplement usage verbose
    # if output_component.usage:
    #     json_output["USAGE"] = {**verbose_usage(complete_device=output_component,
    #                                             input_device=input_component)}

    for attr, val in component.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if attr == "usage":
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
