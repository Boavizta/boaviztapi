from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component
from boaviztapi.model.impact import IMPACT_CRITERIAS
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.bottom_up import get_model_single_impact, NOT_IMPLEMENTED


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


def verbose_usage(device: [Device, Component]):
    json_output = {"use": {}}

    for criteria in IMPACT_CRITERIAS:
        json_output["use"][criteria.name] = {}
        single_impact = get_model_single_impact(device, 'use', 'gwp', 1, Allocation.TOTAL)
        json_output["use"][criteria.name] = single_impact.to_json() if single_impact else NOT_IMPLEMENTED
        json_output["use"][criteria.name]["unit"] = criteria.unit
        json_output["use"][criteria.name]["description"] = criteria.description

    json_output = {**json_output, **iter_boattribute(device.usage)}
    if device.usage.consumption_profile is not None:
        json_output = {**json_output, **iter_boattribute(device.usage.consumption_profile)}

    return json_output


def verbose_component(component: Component):
    json_output = {"units": component.units, "manufacture": {}}
    for criteria in IMPACT_CRITERIAS:
        json_output["manufacture"][criteria.name] = {}
        single_impact = get_model_single_impact(component, "manufacture", criteria.name)
        json_output["manufacture"][criteria.name] = single_impact.to_json() if single_impact else NOT_IMPLEMENTED
        json_output["manufacture"][criteria.name]["unit"] = criteria.unit
        json_output["manufacture"][criteria.name]["description"] = criteria.description

    json_output = {**json_output, **iter_boattribute(component)}

    if component.usage.hours_electrical_consumption.is_set():
        json_output["USAGE"] = verbose_usage(component)

    return json_output


def iter_boattribute(element):
    json_output = {}
    for attr, val in element.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if val.is_set():
            json_output[attr] = val.to_json()
    return json_output