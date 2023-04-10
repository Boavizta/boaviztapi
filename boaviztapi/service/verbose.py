from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.component import Component
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.bottom_up import bottom_up


def verbose_device(device: Device, allocation=Allocation.TOTAL, selected_criteria=config["default_criteria"]):
    json_output = {}
    for component in device.components:
        if f"{component.NAME}-1" in json_output:
            i = 2
            while f"{component.NAME}-{i}" in json_output:
                i += 1
            key = f"{component.NAME}-{i}"
        else:
            key = f"{component.NAME}-1"

        json_output[key] = verbose_component(component, allocation=allocation, selected_criteria=selected_criteria)

    json_output = {**json_output, **verbose_usage(device)}

    return json_output


def verbose_usage(device: [Device, Component]):
    json_output = {**iter_boattribute(device.usage)}
    if device.usage.consumption_profile is not None:
        json_output = {**json_output, **iter_boattribute(device.usage.consumption_profile)}
    for elec in device.usage.elec_factors:
        if device.usage.elec_factors[elec].is_set():
            json_output[f"{elec}_factor"] = device.usage.elec_factors[elec].to_json()

    return json_output


def verbose_component(component: Component, allocation=Allocation.TOTAL, selected_criteria=config["default_criteria"]):
    json_output = {"impacts": bottom_up(component, allocation, selected_criteria), **iter_boattribute(component)}

    if component.usage.hours_electrical_consumption.is_set():
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