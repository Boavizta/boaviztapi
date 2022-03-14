from boaviztapi.model.components.component import Component
from boaviztapi.model.devices.device import Device
import boaviztapi.utils.roundit as rd


def verbose_device(complete_device: Device, input_device: Device):
    json_output = {}

    input_components = input_device.config_components
    complete_components = complete_device.config_components

    input_components.append(input_device.usage)
    complete_components.append(complete_device.usage)

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
                                       **verbose_component(complete_component=complete_component,
                                                           input_component=matching_component)}

    for item in json_output:
        json_output[item]["impacts"]["gwp"] = {'value':json_output[item]["impacts"]["gwp"]['value'] * json_output[item]["unit"], 'unit':json_output[item]["impacts"]["gwp"]['unit']}
        json_output[item]["impacts"]["pe"] = {'value':json_output[item]["impacts"]["pe"]['value'] * json_output[item]["unit"], 'unit':json_output[item]["impacts"]["gwp"]['unit']}
        json_output[item]["impacts"]["adp"] = {'value':json_output[item]["impacts"]["adp"]['value'] * json_output[item]["unit"], 'unit':json_output[item]["impacts"]["gwp"]['unit']}

    return json_output


def verbose_component(complete_component: Component, input_component: Component):
    json_output = {}

    for attr, value in complete_component.__iter__():
        if type(value) is dict:
            json_output[attr] = \
                recursive_dict_verbose(value,
                                       {} if getattr(input_component, attr) is None else getattr(input_component, attr))
        elif value is not None and attr != "TYPE" and attr != "hash":
            json_output[attr] = {}
            json_output[attr]["input_value"] = getattr(input_component, attr, None)
            json_output[attr]["used_value"] = value
            json_output[attr]["status"] = get_status(json_output[attr]["used_value"], json_output[attr]["input_value"])

    json_output["impacts"] = {"gwp":{
                                    "value": rd.round_to_sigfig(*complete_component.impact_gwp()),
                                    "unit": "kgCO2eq"},
                              "pe": {
                                  "value": rd.round_to_sigfig(*complete_component.impact_pe()),
                        "unit": "MJ"},
                              "adp": {"value": rd.round_to_sigfig(*complete_component.impact_adp()),
                                      "unit": "kgSbeq"},
                                      }
    return json_output


def recursive_dict_verbose(dict1, dict2):
    json_output = {}
    for attr, value in dict1.items():
        if type(value) is dict:
            json_output[attr] = recursive_dict_verbose(value, dict2.get(attr, {}))
        elif value is not None:
            json_output[attr] = {}
            json_output[attr]["input_value"] = dict2.get(attr)
            json_output[attr]["used_value"] = value
            json_output[attr]["status"] = get_status(json_output[attr]["used_value"], json_output[attr]["input_value"])
    return json_output


def get_status(usedt_value, input_value):
    if usedt_value == input_value:
        return "UNCHANGED"
    elif input_value is None:
        return "SET"
    else:
        return "MODIFY"
