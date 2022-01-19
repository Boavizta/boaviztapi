import copy

from fastapi import APIRouter, Body

from boaviztapi.model.components.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentMotherBoard, ComponentPowerSupply, ComponentRack, ComponentBlade
from boaviztapi.routers.openapi_doc.descriptions import cpu_description, ram_description, ssd_description, \
    hdd_description, motherboard_description, power_supply_description, rack_description, blade_description
from boaviztapi.routers.openapi_doc.examples import components_examples
from boaviztapi.service.bottom_up import bottom_up_component
from boaviztapi.service.verbose import verbose_component

component_router = APIRouter(
    prefix='/v1/component',
    tags=['component']
)


@component_router.post('/cpu',
                       description=cpu_description)
def cpu_impact_bottom_up(cpu: ComponentCPU = Body(None, example=components_examples["cpu"]), verbose: bool = True):
    completed_cpu = copy.deepcopy(cpu)
    impacts = bottom_up_component(component=completed_cpu)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_cpu, cpu)}
    return result


@component_router.post('/ram',
                       description=ram_description)
def ram_impact_bottom_up(ram: ComponentRAM = Body(None, example=components_examples["ram"]), verbose: bool = True):
    completed_ram = copy.deepcopy(ram)
    impacts = bottom_up_component(component=completed_ram)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_ram, ram)}
    return result


@component_router.post('/ssd',
                       description=ssd_description)
def ssd_impact_bottom_up(ssd: ComponentSSD = Body(None, example=components_examples["ssd"]), verbose: bool = True):
    completed_ssd = copy.deepcopy(ssd)
    impacts = bottom_up_component(component=completed_ssd)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_ssd, ssd)}
    return result


@component_router.post('/hdd',
                       description=hdd_description)
def hdd_impact_bottom_up(hdd: ComponentHDD = Body(None, example=components_examples["hdd"]), verbose: bool = True):
    completed_hdd = copy.deepcopy(hdd)
    impacts = bottom_up_component(component=completed_hdd)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_hdd, hdd)}
    return result


@component_router.post('/motherboard',
                       description=motherboard_description)
def motherboard_impact_bottom_up(motherboard: ComponentMotherBoard
                                 = Body(None, example=components_examples["motherboard"]), verbose: bool = True):
    completed_motherboard = copy.deepcopy(motherboard)
    impacts = bottom_up_component(component=completed_motherboard)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_motherboard, motherboard)}
    return result


@component_router.post('/power_supply',
                       description=power_supply_description)
def power_supply_impact_bottom_up(power_supply: ComponentPowerSupply =
                                  Body(None, example=components_examples["power_supply"]), verbose: bool = True):
    completed_power_supply = copy.deepcopy(power_supply)
    impacts = bottom_up_component(component=completed_power_supply)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_power_supply, power_supply)}
    return result


@component_router.post('/rack',
                       description=rack_description)
def rack_impact_bottom_up(rack: ComponentRack = Body(None, example=components_examples["rack"]), verbose: bool = True):
    completed_rack = copy.deepcopy(rack)
    impacts = bottom_up_component(component=completed_rack)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_rack, rack)}
    return result


@component_router.post('/blade',
                       description=blade_description)
def blade_impact_bottom_up(blade: ComponentBlade = Body(None, example=components_examples["blade"]),
                           verbose: bool = True):
    completed_blade = copy.deepcopy(blade)
    impacts = bottom_up_component(component=completed_blade)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_blade, blade)}
    return result
