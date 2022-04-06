import copy

from fastapi import APIRouter, Body

from boaviztapi.dto.component_dto import Cpu, Ram, Disk, PowerSupply, MotherBoard, Case
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
async def cpu_impact_bottom_up(cpu: Cpu = Body(None, example=components_examples["cpu"]), verbose: bool = True):
    component_cpu = cpu.to_component()
    completed_cpu = copy.deepcopy(component_cpu)
    impacts = bottom_up_component(component=completed_cpu, units=cpu.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_cpu, component_cpu, units=cpu.units or 1)}
    return result


@component_router.post('/ram',
                       description=ram_description)
async def ram_impact_bottom_up(ram: Ram = Body(None, example=components_examples["ram"]),
                               verbose: bool = True):
    component_ram = ram.to_component()
    completed_ram = copy.deepcopy(component_ram)
    impacts = bottom_up_component(component=completed_ram, units=ram.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_ram, component_ram, units=ram.units or 1)}
    return result


@component_router.post('/ssd',
                       description=ssd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["ssd"]),
                                verbose: bool = True):
    disk.type = "ssd"
    component_disk = disk.to_component()
    completed_disk = copy.deepcopy(component_disk)
    impacts = bottom_up_component(component=completed_disk, units=disk.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_disk, component_disk, units=disk.units or 1)}
    return result


@component_router.post('/hdd',
                       description=hdd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["hdd"]),
                                verbose: bool = True):
    disk.type = "hdd"
    disk_component = disk.to_component()
    completed_disk = copy.deepcopy(disk_component)
    impacts = bottom_up_component(component=completed_disk, units=disk.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_disk, disk_component, units=disk.units or 1)}
    return result


@component_router.post('/motherboard',
                       description=motherboard_description)
async def motherboard_impact_bottom_up(motherboard: MotherBoard
                                       = Body(None, example=components_examples["motherboard"]), verbose: bool = True):
    component_motherboard = motherboard.to_component()
    completed_motherboard = copy.deepcopy(component_motherboard)
    impacts = bottom_up_component(component=completed_motherboard, units=motherboard.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_motherboard, completed_motherboard, units=motherboard.units or 1)}
    return result


@component_router.post('/power_supply',
                       description=power_supply_description)
async def power_supply_impact_bottom_up(power_supply: PowerSupply =
                                        Body(None, example=components_examples["power_supply"]), verbose: bool = True):
    component_power_supply = power_supply.to_component()
    completed_power_supply = copy.deepcopy(component_power_supply)
    impacts = bottom_up_component(component=completed_power_supply, units=power_supply.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_power_supply, component_power_supply, units=power_supply.units or 1)}
    return result


@component_router.post('/case',
                       description=case_description)
async def case_impact_bottom_up(case: Case = Body(None, example=components_examples["case"]),
                                verbose: bool = True):
    component_case = case.to_component()
    completed_case = copy.deepcopy(component_case)
    impacts = bottom_up_component(component=completed_case, units=case.units or 1)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(completed_case, component_case, units=case.units or 1)}
    return result
