from typing import List

from api.model.components.component import Component


def verbose_components(input_components: List[Component], complete_components: List[Component]):
    json_output = {}
    matching_complete_component = None

    for component in input_components:
        component_type = component.TYPE
        done = False
        i = 1

        while True:
            component_name = component_type + "-" + str(i)
            if json_output.get(component_name) is None:
                json_output[component_name] = {}
                json_output[component_name]["unit"] = 1
                break
            elif component.hash == json_output[component_name].get("hash"):
                json_output[component_name]["unit"] += 1
                done = True
                break
            i += 1
        if done:
            continue

        for item in complete_components:
            if component.hash == item.hash:
                matching_complete_component = item
                break

        json_output[component_name]["hash"] = component.hash

        json_output[component_name] = {**json_output[component_name],
                                       **verbose_component(component, matching_complete_component)}

    for item in json_output:
        json_output[item]["impacts"]["gwp"] =  round(json_output[item]["impacts"]["gwp"] * json_output[item]["unit"], 0)
        json_output[item]["impacts"]["pe"] = round(json_output[item]["impacts"]["pe"] * json_output[item]["unit"], 0)
        json_output[item]["impacts"]["adp"] = round(json_output[item]["impacts"]["adp"] * json_output[item]["unit"], 3)

    return json_output


def verbose_component(input_component: Component, complete_component: Component):
    json_output = {}

    for attr, value in input_component.__iter__():
        if not (value is None and getattr(complete_component, attr) is None) and (attr != "TYPE" and attr != "hash"):
            json_output[attr] = {}
            json_output[attr]["input_value"] = value
            json_output[attr]["used_value"] = getattr(complete_component, attr)

            if json_output[attr]["used_value"] == json_output[attr]["input_value"]:
                json_output[attr]["status"] = "UNCHANGED"

            elif json_output[attr]["input_value"] is None:
                json_output[attr]["status"] = "SET"

            else:
                json_output[attr]["status"] = "MODIFY"

    json_output["impacts"] = {"gwp": complete_component.impact_gwp(),
                              "pe": complete_component.impact_pe(),
                              "adp": complete_component.impact_adp()}
    return json_output
