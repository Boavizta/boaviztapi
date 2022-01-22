import copy

from fastapi import APIRouter, Body

from boaviztapi.model.components.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentMotherBoard, ComponentPowerSupply, ComponentCase
from boaviztapi.routers.openapi_doc.descriptions import cpu_description, ram_description, ssd_description, \
    hdd_description, motherboard_description, power_supply_description, case_description
from boaviztapi.routers.openapi_doc.examples import components_examples
from boaviztapi.service.bottom_up import bottom_up_component
from boaviztapi.service.verbose import verbose_component

component_router = APIRouter(
    prefix='/v1/component',
    tags=['component']
)


@component_router.post('/cpu',
                       description=cpu_description)
async def cpu_impact_bottom_up(cpu: ComponentCPU = Body(None, example=components_examples["cpu"]), verbose: bool = True):
    completed_cpu = copy.deepcopy(cpu)
    impacts = bottom_up_component(component=completed_cpu)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_cpu, cpu)}
    return result


@component_router.post('/ram',
                       description=ram_description)
async def ram_impact_bottom_up(ram: ComponentRAM = Body(None, example=components_examples["ram"]), verbose: bool = True):
    completed_ram = copy.deepcopy(ram)
    impacts = bottom_up_component(component=completed_ram)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_ram, ram)}
    return result


@component_router.post('/ssd',
                       description=ssd_description)
async def ssd_impact_bottom_up(ssd: ComponentSSD = Body(None, example=components_examples["ssd"]), verbose: bool = True):
    completed_ssd = copy.deepcopy(ssd)
    impacts = bottom_up_component(component=completed_ssd)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_ssd, ssd)}
    return result


@component_router.post('/hdd',
                       description=hdd_description)
async def hdd_impact_bottom_up(hdd: ComponentHDD = Body(None, example=components_examples["hdd"]), verbose: bool = True):
    completed_hdd = copy.deepcopy(hdd)
    impacts = bottom_up_component(component=completed_hdd)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_hdd, hdd)}
    return result


@component_router.post('/motherboard',
                       description=motherboard_description)
async def motherboard_impact_bottom_up(motherboard: ComponentMotherBoard
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
async def power_supply_impact_bottom_up(power_supply: ComponentPowerSupply =
                                  Body(None, example=components_examples["power_supply"]), verbose: bool = True):
    completed_power_supply = copy.deepcopy(power_supply)
    impacts = bottom_up_component(component=completed_power_supply)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_power_supply, power_supply)}
    return result


@component_router.post('/case',
                       description=case_description)
async def case_impact_bottom_up(case: ComponentCase = Body(None, example=components_examples["case"]),
                          verbose: bool = True):
    completed_case = copy.deepcopy(case)
    impacts = bottom_up_component(component=completed_case)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_case, case)}
    return result
