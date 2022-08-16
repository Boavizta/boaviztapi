from fastapi import APIRouter, Body

from boaviztapi.dto.component import CPU, RAM, Disk, PowerSupply, Motherboard, Case
from boaviztapi.dto.component.cpu import smart_mapper_cpu
from boaviztapi.dto.component.other import mapper_motherboard, mapper_power_supply, mapper_case
from boaviztapi.dto.component.ram import smart_mapper_ram
from boaviztapi.dto.component.disk import smart_mapper_ssd, mapper_hdd
from boaviztapi.model.component import Component
from boaviztapi.routers.openapi_doc.descriptions import cpu_description, ram_description, ssd_description, \
    hdd_description, motherboard_description, power_supply_description, case_description
from boaviztapi.routers.openapi_doc.examples import components_examples
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.bottom_up import bottom_up_component
from boaviztapi.service.verbose import verbose_component

component_router = APIRouter(
    prefix='/v1/component',
    tags=['component']
)


@component_router.post('/cpu',
                       description=cpu_description)
async def cpu_impact_bottom_up(cpu: CPU = Body(None, example=components_examples["cpu"]),
                               verbose: bool = True,
                               allocation: Allocation = Allocation.TOTAL):

    component = smart_mapper_cpu(cpu)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        allocation=allocation
    )


@component_router.post('/ram',
                       description=ram_description)
async def ram_impact_bottom_up(ram: RAM = Body(None, example=components_examples["ram"]),
                               verbose: bool = True,
                               allocation: Allocation = Allocation.TOTAL):

    completed_ram = smart_mapper_ram(ram)

    return await component_impact_bottom_up(
        component=completed_ram,
        verbose=verbose,
        allocation=allocation
    )


@component_router.post('/ssd',
                       description=ssd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["ssd"]),
                                verbose: bool = True,
                                allocation: Allocation = Allocation.TOTAL):
    disk.type = "ssd"
    competed_ssd = smart_mapper_ssd(disk)

    return await component_impact_bottom_up(
        component=competed_ssd,
        verbose=verbose,
        allocation=allocation
    )


@component_router.post('/hdd',
                       description=hdd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["hdd"]),
                                verbose: bool = True,
                                allocation: Allocation = Allocation.TOTAL):
    disk.type = "hdd"
    component = mapper_hdd(disk)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        allocation=allocation
    )


@component_router.post('/motherboard',
                       description=motherboard_description)
async def motherboard_impact_bottom_up(
        motherboard: Motherboard = Body(None, example=components_examples["motherboard"]),
        verbose: bool = True, allocation: Allocation = Allocation.TOTAL):

    completed_motherboard = mapper_motherboard(motherboard)

    return await component_impact_bottom_up(
        component=completed_motherboard,
        verbose=verbose,
        allocation=allocation
    )


@component_router.post('/power_supply',
                       description=power_supply_description)
async def power_supply_impact_bottom_up(
        power_supply: PowerSupply = Body(None, example=components_examples["power_supply"]),
        verbose: bool = True, allocation: Allocation = Allocation.TOTAL):

    completed_power_supply = mapper_power_supply(power_supply)

    return await component_impact_bottom_up(
        component=completed_power_supply,
        verbose=verbose,
        allocation=allocation
    )


@component_router.post('/case',
                       description=case_description)
async def case_impact_bottom_up(case: Case = Body(None, example=components_examples["case"]),
                                verbose: bool = True,
                                allocation: Allocation = Allocation.TOTAL):

    completed_case = mapper_case(case)

    return await component_impact_bottom_up(
        component=completed_case,
        verbose=verbose,
        allocation=allocation
    )


async def component_impact_bottom_up(component: Component,
                                     verbose: bool, allocation: Allocation) -> dict:

    impacts = bottom_up_component(component=component, allocation=allocation)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_component(component=component)
        }
    return impacts
