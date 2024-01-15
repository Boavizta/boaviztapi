import os
from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from boaviztapi import config, data_dir
from boaviztapi.dto.component import CPU, RAM, Disk, PowerSupply, Motherboard, Case
from boaviztapi.dto.component.cpu import mapper_cpu
from boaviztapi.dto.component.other import mapper_motherboard, mapper_power_supply, mapper_case
from boaviztapi.dto.component.ram import mapper_ram
from boaviztapi.dto.component.disk import mapper_ssd, mapper_hdd
from boaviztapi.model.component import Component
from boaviztapi.routers.openapi_doc.descriptions import cpu_description, ram_description, ssd_description, \
    hdd_description, motherboard_description, power_supply_description, case_description
from boaviztapi.routers.openapi_doc.examples import components_examples
from boaviztapi.service.archetype import get_component_archetype, get_device_archetype_lst
from boaviztapi.service.impacts_computation import compute_impacts
from boaviztapi.service.verbose import verbose_component

component_router = APIRouter(
    prefix='/v1/component',
    tags=['component']
)


@component_router.get('/all',
                      description=cpu_description)
async def cpu_all_archetype_name():
    return {
        "cpu": "v1/component/cpu",
        "ram": "v1/component/ram",
        "ssd": "v1/component/ssd",
        "hdd": "v1/component/hdd",
        "motherboard": "v1/component/motherboard",
        "power_supply": "v1/component/power_supply",
        "case": "v1/component/case"
    }


@component_router.get('/cpu/archetype',
                      description=cpu_description)
async def cpu_all_archetype_name():
    archetype_lst = get_all_archetype_name("cpu")
    return archetype_lst


@component_router.get('/cpu/archetype_config',
                      description=cpu_description)
async def cpu_archetype_config(archetype: str = Query(example=config["default_cpu"])):
    archetype_config = get_archetype_config(archetype, "cpu")
    return archetype_config


@component_router.post('/cpu',
                       description=cpu_description)
async def cpu_impact_bottom_up(cpu: CPU = Body(None, example=components_examples["cpu"]),
                               verbose: bool = True,
                               duration: Optional[float] = config["default_duration"],
                               archetype: str = config["default_cpu"],
                               criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "cpu")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_cpu(cpu, archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/cpu',
                      description=cpu_description)
async def cpu_impact_bottom_up(verbose: bool = True,
                               duration: Optional[float] = config["default_duration"],
                               archetype: str = config["default_cpu"],
                               criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "cpu")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_cpu(CPU(), archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/ram/archetype',
                      description=ram_description)
async def ram_all_archetype_name():
    archetype_lst = get_all_archetype_name("ram")
    return archetype_lst


@component_router.get('/ram/archetype_config',
                      description=ram_description)
async def ram_archetype_config(archetype: str = Query(example=config["default_ram"])):
    archetype_config = get_archetype_config(archetype, "ram")
    return archetype_config


@component_router.post('/ram',
                       description=ram_description)
async def ram_impact_bottom_up(ram: RAM = Body(None, example=components_examples["ram"]),
                               verbose: bool = True,
                               duration: Optional[float] = config["default_duration"],
                               archetype: str = config["default_ram"],
                               criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "ram")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_ram(ram, archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/ram',
                      description=ram_description)
async def ram_impact_bottom_up(verbose: bool = True,
                               duration: Optional[float] = config["default_duration"],
                               archetype: str = config["default_ram"],
                               criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "ram")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_ram(RAM(), archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/ssd/archetype',
                      description=ssd_description)
async def ssd_all_archetype_name():
    archetype_lst = get_all_archetype_name("ssd")
    return archetype_lst


@component_router.get('/ssd/archetype_config',
                      description=ssd_description)
async def ssd_archetype_config(archetype: str = Query(example=config["default_ssd"])):
    archetype_config = get_archetype_config(archetype, "ssd")
    return archetype_config


@component_router.post('/ssd',
                       description=ssd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["ssd"]),
                                verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                archetype: str = config["default_ssd"],
                                criteria: List[str] = Query(config["default_criteria"])):
    disk.type = "ssd"
    archetype_config = get_component_archetype(archetype, "ssd")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_ssd(disk, archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/ssd',
                      description=ssd_description)
async def disk_impact_bottom_up(verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                archetype: str = config["default_ssd"],
                                criteria: List[str] = Query(config["default_criteria"])):
    disk = Disk()
    disk.type = "ssd"
    archetype_config = get_component_archetype(archetype, "ssd")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_ssd(disk, archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/hdd/archetype',
                      description=hdd_description)
async def hdd_all_archetype_name():
    archetype_lst = get_all_archetype_name("hdd")
    return archetype_lst


@component_router.get('/hdd/archetype_config',
                      description=hdd_description)
async def hdd_archetype_config(archetype: str = Query(example=config["default_hdd"])):
    archetype_config = get_archetype_config(archetype, "hdd")
    return archetype_config


@component_router.post('/hdd',
                       description=hdd_description)
async def disk_impact_bottom_up(disk: Disk = Body(None, example=components_examples["hdd"]),
                                verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                archetype: str = config["default_hdd"],
                                criteria: List[str] = Query(config["default_criteria"])):
    disk.type = "hdd"
    archetype_config = get_component_archetype(archetype, "hdd")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_hdd(disk, archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/hdd',
                      description=hdd_description)
async def disk_impact_bottom_up(verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                archetype: str = config["default_hdd"],
                                criteria: List[str] = Query(config["default_criteria"])):
    disk = Disk()
    disk.type = "hdd"
    archetype_config = get_component_archetype(archetype, "hdd")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    component = mapper_hdd(disk, archetype_config)

    return await component_impact_bottom_up(
        component=component,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/motherboard/archetype',
                      description=motherboard_description)
async def motherboard_all_archetype_name():
    archetype_lst = get_all_archetype_name("motherboard")
    return archetype_lst


@component_router.get('/motherboard/archetype_config',
                      description=motherboard_description)
async def motherboard_archetype_config(archetype: str = Query(example=config["default_motherboard"])):
    archetype_config = get_archetype_config(archetype, "motherboard")
    return archetype_config


@component_router.post('/motherboard',
                       description=motherboard_description)
async def motherboard_impact_bottom_up(
        motherboard: Motherboard = Body(None, example=components_examples["motherboard"]),
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])):
    completed_motherboard = mapper_motherboard(motherboard)

    return await component_impact_bottom_up(
        component=completed_motherboard,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/motherboard',
                      description=motherboard_description)
async def motherboard_impact_bottom_up(verbose: bool = True,
                                       duration: Optional[float] = config["default_duration"],
                                       criteria: List[str] = Query(config["default_criteria"])):
    completed_motherboard = mapper_motherboard(Motherboard())

    return await component_impact_bottom_up(
        component=completed_motherboard,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/power_supply/archetype',
                      description=power_supply_description)
async def power_supply_all_archetype_name():
    archetype_lst = get_all_archetype_name("power_supply")
    return archetype_lst


@component_router.get('/power_supply/archetype_config',
                      description=power_supply_description)
async def power_supply_archetype_config(archetype: str = Query(example=config["default_power_supply"])):
    archetype_config = get_archetype_config(archetype, "power_supply")
    return archetype_config


@component_router.post('/power_supply',
                       description=power_supply_description)
async def power_supply_impact_bottom_up(
        power_supply: PowerSupply = Body(None, example=components_examples["power_supply"]),
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        archetype: str = config["default_power_supply"],
        criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "power_supply")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    completed_power_supply = mapper_power_supply(power_supply, archetype_config)

    return await component_impact_bottom_up(
        component=completed_power_supply,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/power_supply',
                      description=power_supply_description)
async def power_supply_impact_bottom_up(verbose: bool = True,
                                        duration: Optional[float] = config["default_duration"],
                                        archetype: str = config["default_power_supply"],
                                        criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "power_supply")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    completed_power_supply = mapper_power_supply(PowerSupply(), archetype_config)

    return await component_impact_bottom_up(
        component=completed_power_supply,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/case/archetype',
                      description=case_description)
async def case_all_archetype_name():
    archetype_lst = get_all_archetype_name("case")
    return archetype_lst


@component_router.get('/case/archetype_config',
                      description=case_description)
async def case_archetype_config(archetype: str = Query(example=config["default_case"])):
    archetype_config = get_archetype_config(archetype, "case")
    return archetype_config


@component_router.post('/case',
                       description=case_description)
async def case_impact_bottom_up(case: Case = Body(None, example=components_examples["case"]),
                                verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                archetype: str = config["default_case"],
                                criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "case")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    completed_case = mapper_case(case, archetype_config)

    return await component_impact_bottom_up(
        component=completed_case,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@component_router.get('/case',
                      description=case_description)
async def case_impact_bottom_up(verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                archetype: str = config["default_case"],
                                criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_component_archetype(archetype, "case")

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    completed_case = mapper_case(Case(), archetype_config)

    return await component_impact_bottom_up(
        component=completed_case,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


async def component_impact_bottom_up(component: Component,
                                     verbose: bool,
                                     duration: Optional[float] = config["default_duration"],
                                     criteria=config["default_criteria"]) -> dict:
    if duration is None:
        duration = component.usage.hours_life_time.value

    impacts = compute_impacts(model=component, duration=duration, selected_criteria=criteria)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_component(component=component, duration=duration)
        }
    return {"impacts": impacts}


def get_all_archetype_name(name: str):
    return get_device_archetype_lst(os.path.join(data_dir, f'archetypes/components/{name.lower()}.csv'))


def get_archetype_config(archetype: str, component_type: str):
    result = get_component_archetype(archetype, component_type)
    if not result:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")
    return result
