from boaviztapi.model.components.component import Component
from boaviztapi.model.devices.device import Device


def verbose_device(complete_device: Device, input_device: Device):
    json_output = {}

    # if complete_device.usage:
    #     complete_device.config_components.append(complete_device.usage)
    #     input_device.config_components.append(input_device.usage)

    input_components = input_device.config_components
    complete_components = complete_device.config_components

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
        json_output[item]["impacts"]["gwp"] = round(json_output[item]["impacts"]["gwp"] * json_output[item]["unit"], 0)
        json_output[item]["impacts"]["pe"] = round(json_output[item]["impacts"]["pe"] * json_output[item]["unit"], 0)
        json_output[item]["impacts"]["adp"] = round(json_output[item]["impacts"]["adp"] * json_output[item]["unit"], 3)

    return json_output


def verbose_component(complete_component: Component, input_component: Component):
    json_output = {}

    for attr, value in complete_component.__iter__():
        if value is not None and attr != "TYPE" and attr != "hash":
            json_output[attr] = {}
            json_output[attr]["input_value"] = getattr(input_component, attr, None)
            json_output[attr]["used_value"] = value

            if json_output[attr]["used_value"] == json_output[attr]["input_value"]:
                json_output[attr]["status"] = "UNCHANGED"

            elif json_output[attr]["input_value"] is None:
                json_output[attr]["status"] = "SET"

            else:
                json_output[attr]["status"] = "MODIFY"

    json_output["impacts"] = {"gwp": round(complete_component.impact_gwp(), 0),
                              "pe": round(complete_component.impact_pe(), 0),
                              "adp": round(complete_component.impact_adp(), 3)}
    return json_output
