import json

import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Status
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.device import DeviceDTO


def verbose_device(input_device_dto: DeviceDTO, output_device_dto: DeviceDTO):
    json_output = {}
    # if complete_device.usage:
    #     json_output["USAGE"] = {**verbose_usage(complete_device=complete_device,
    #                                             input_device=input_device)}

    input_components = input_device_dto.config_components
    complete_components = output_device_dto.config_components

    for complete_component in complete_components:
        component_type = complete_component.TYPE
        done = False
        i = 1

        while True:
            component_name = component_type + "-" + str(i)
            if json_output.get(component_name) is None:
                json_output[component_name] = {}
                json_output[component_name]["unit"] = 1
                break
            elif complete_component.hash == json_output[component_name].get("hash"):
                json_output[component_name]["unit"] += 1
                done = True
                break
            i += 1
        if done:
            continue

        matching_component = None
        for item in input_components:
            if complete_component.hash == item.hash:
                matching_component = item
                break

        json_output[component_name]["hash"] = complete_component.hash

        json_output[component_name] = {**json_output[component_name],
                                       **verbose_component(output_component_dto=complete_component,
                                                           input_component_dto=matching_component)}

    for item in json_output:
        json_output[item]["impacts"]["gwp"] = {
            'value': json_output[item]["impacts"]["gwp"]['value'] * json_output[item]["unit"],
            'unit': "kgCO2eq"
        }
        json_output[item]["impacts"]["pe"] = {
            'value': json_output[item]["impacts"]["pe"]['value'] * json_output[item]["unit"],
            'unit': "MJ"
        }
        json_output[item]["impacts"]["adp"] = {
            'value': json_output[item]["impacts"]["adp"]['value'] * json_output[item]["unit"],
            'unit': "kgSbeq"
        }
    return json_output


def verbose_usage(complete_device, input_device):
    json_output = {"unit": 1}

    for attr, value in complete_device.usage.__iter__():
        if type(value) is dict:
            json_output[attr] = \
                recursive_dict_verbose(value,
                                       {} if getattr(input_device.usage, attr) is None else getattr(input_device.usage, attr))
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


def verbose_component(component: Component,
                      units: int = None):
    json_output = {}
    # TODO: Reimplement usage verbose
    # if output_component.usage:
    #     json_output["USAGE"] = {**verbose_usage(complete_device=output_component,
    #                                             input_device=input_component)}
    if units:
        json_output["units"] = units

    for attr, val in component.__iter__():
        if attr == "usage":
            continue
        if val.status != Status.NONE:
            json_output[attr.rsplit('__', 1)[1]] = val

    json_output["impacts"] = {
        "gwp": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_gwp()),
            "unit": "kgCO2eq"
        },
        "pe": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_pe()),
            "unit": "MJ"},
        "adp": {
            "value": rd.round_to_sigfig(*component.impact_manufacture_adp()),
            "unit": "kgSbeq"
        },
    }
    return json_output
