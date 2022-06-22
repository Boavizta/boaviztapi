from typing import Type

from fastapi import APIRouter, Body

from boaviztapi.dto.component import ComponentDTO, CPU, RAM, Disk, PowerSupply, Motherboard, Case
from boaviztapi.dto.component.cpu import smart_complete_cpu
from boaviztapi.dto.component.ram import smart_complete_ram
from boaviztapi.dto.component.disk import smart_complete_disk_ssd
from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentHDD, ComponentSSD, \
    ComponentPowerSupply, ComponentMotherboard, ComponentCase
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
async def cpu_impact_bottom_up(cpu: CPU = Body(None, example=components_examples["cpu"]), verbose: bool = True):
    completed_cpu = smart_complete_cpu(cpu)
    return await component_impact_bottom_up(
        input_component_dto=cpu,
        smart_complete_component_dto=completed_cpu,
        component_class=ComponentCPU,
        verbose=verbose
    )


@component_router.post('/ram',
                       description=ram_description)
async def ram_impact_bottom_up(ram: RAM = Body(None, example=components_examples["ram"]), verbose: bool = True):
    completed_ram = smart_complete_ram(ram)

    return await component_impact_bottom_up(
        input_component_dto=ram,
        smart_complete_component_dto=completed_ram,
        component_class=ComponentRAM,
        verbose=verbose
    )


@component_router.post('/ssd',
                       description=ssd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["ssd"]), verbose: bool = True):
    disk.type = "ssd"
    competed_ssd = smart_complete_disk_ssd(disk)
    return await component_impact_bottom_up(
        input_component_dto=disk,
        smart_complete_component_dto=competed_ssd,
        component_class=ComponentSSD,
        verbose=verbose
    )


@component_router.post('/hdd',
                       description=hdd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["hdd"]), verbose: bool = True):
    disk.type = "hdd"
    completed_hdd = disk.copy()
    return await component_impact_bottom_up(
        input_component_dto=disk,
        smart_complete_component_dto=completed_hdd,
        component_class=ComponentHDD,
        verbose=verbose
    )


@component_router.post('/motherboard',
                       description=motherboard_description)
async def motherboard_impact_bottom_up(
        motherboard: Motherboard = Body(None, example=components_examples["motherboard"]),
        verbose: bool = True):
    completed_motherboard = motherboard.copy()
    return await component_impact_bottom_up(
        input_component_dto=motherboard,
        smart_complete_component_dto=completed_motherboard,
        component_class=ComponentMotherboard,
        verbose=verbose
    )


@component_router.post('/power_supply',
                       description=power_supply_description)
async def power_supply_impact_bottom_up(
        power_supply: PowerSupply = Body(None, example=components_examples["power_supply"]),
        verbose: bool = True):
    completed_power_supply = power_supply.copy()
    return await component_impact_bottom_up(
        input_component_dto=power_supply,
        smart_complete_component_dto=completed_power_supply,
        component_class=ComponentPowerSupply,
        verbose=verbose
    )


@component_router.post('/case',
                       description=case_description)
async def case_impact_bottom_up(case: Case = Body(None, example=components_examples["case"]), verbose: bool = True):
    completed_case = case.copy()
    return await component_impact_bottom_up(
        input_component_dto=case,
        smart_complete_component_dto=completed_case,
        component_class=ComponentCase,
        verbose=verbose
    )


async def component_impact_bottom_up(input_component_dto: ComponentDTO,
                                     smart_complete_component_dto: ComponentDTO,
                                     component_class: Type[Component],
                                     verbose: bool) -> dict:
    component = component_class.from_dto(smart_complete_component_dto, input_component_dto)
    impacts = bottom_up_component(component=component)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_component(component=component)
        }
    return impacts
