from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component
from boaviztapi.service.bottom_up import bottom_up


def verbose_device(device: Device, selected_criteria=config["default_criteria"], duration=config["default_duration"]):
    json_output = {"duration": {"value":duration, "unit": "hours"}}
    for component in device.components:
        component.usage.hours_life_time.set_completed(device.usage.hours_life_time.value, min=device.usage.hours_life_time.min, max=device.usage.hours_life_time.max, source="from device")
        if f"{component.NAME}-1" in json_output:
            i = 2
            while f"{component.NAME}-{i}" in json_output:
                i += 1
            key = f"{component.NAME}-{i}"
        else:
            key = f"{component.NAME}-1"

        json_output[key] = verbose_component(component, duration=duration, selected_criteria=selected_criteria)

    json_output = {**json_output, **verbose_usage(device), **iter_boattribute(device)}

    return json_output


def verbose_usage(device: [Device, Component]):
    json_output = {**iter_boattribute(device.usage)}
    if device.usage.consumption_profile is not None:
        if device.usage.consumption_profile.workloads.is_set():
            json_output["workloads"] = device.usage.consumption_profile.workloads.to_json()
            json_output["workloads"]["value"] = [{"load_percentage" : workload.load_percentage, "power_watt": workload.power_watt} for workload in json_output["workloads"]["value"]]
        if device.usage.consumption_profile.params.is_set():
            json_output["params"] = device.usage.consumption_profile.params.to_json()
    for elec in device.usage.elec_factors:
        if device.usage.elec_factors[elec].is_set():
            json_output[f"{elec}_factor"] = device.usage.elec_factors[elec].to_json()

    return json_output


def verbose_component(component: Component, duration=config["default_duration"], selected_criteria=config["default_criteria"]):
    json_output = {"impacts": bottom_up(component, selected_criteria, duration=duration), **iter_boattribute(component), "duration": {"value":duration, "unit": "hours"}}

    if component.usage.avg_power.is_set():
        json_output= {**json_output, **verbose_usage(component)}

    return json_output


def iter_boattribute(element):
    json_output = {}
    for attr, val in element.__iter__():
        if not isinstance(val, Boattribute):
            continue
        if val.is_set():
            json_output[attr] = val.to_json()
    return json_output