import copy

from fastapi import APIRouter

from api.model.components.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentMotherBoard, ComponentPowerSupply, ComponentRack, ComponentBlade
from api.service.bottom_up import bottom_up_component
from api.service.verbose import verbose_component

component_router = APIRouter(
    prefix='/v1/component',
    tags=['component']
)


@component_router.post('/cpu')
def cpu_impact_bottom_up(cpu: ComponentCPU, verbose: bool = True):
    completed_cpu = copy.deepcopy(cpu)
    impacts = bottom_up_component(component=completed_cpu)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(cpu, completed_cpu)}
    return result


@component_router.post('/ram')
def ram_impact_bottom_up(ram: ComponentRAM, verbose: bool = True):
    completed_ram = copy.deepcopy(ram)
    impacts = bottom_up_component(component=completed_ram)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(ram, completed_ram)}
    return result


@component_router.post('/ssd')
def ssd_impact_bottom_up(ssd: ComponentSSD, verbose: bool = True):
    completed_ssd = copy.deepcopy(ssd)
    impacts = bottom_up_component(component=completed_ssd)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(ssd, completed_ssd)}
    return result


@component_router.post('/hdd')
def hdd_impact_bottom_up(hdd: ComponentHDD, verbose: bool = True):
    completed_hdd = copy.deepcopy(hdd)
    impacts = bottom_up_component(component=completed_hdd)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(hdd, completed_hdd)}
    return result


@component_router.post('/motherboard')
def motherboard_impact_bottom_up(motherboard: ComponentMotherBoard, verbose: bool = True):
    completed_motherboard = copy.deepcopy(motherboard)
    impacts = bottom_up_component(component=completed_motherboard)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(motherboard, completed_motherboard)}
    return result


@component_router.post('/power-supply')
def power_supply_impact_bottom_up(power_supply: ComponentPowerSupply, verbose: bool = True):
    completed_power_supply = copy.deepcopy(power_supply)
    impacts = bottom_up_component(component=completed_power_supply)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(power_supply, completed_power_supply)}
    return result


@component_router.post('/rack')
def rack_impact_bottom_up(rack: ComponentRack, verbose: bool = True):
    completed_rack = copy.deepcopy(rack)
    impacts = bottom_up_component(component=completed_rack)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(rack, completed_rack)}
    return result


@component_router.post('/blade')
def blade_impact_bottom_up(blade: ComponentBlade, verbose: bool = True):
    completed_blade = copy.deepcopy(blade)
    impacts = bottom_up_component(component=completed_blade)
    result = impacts
    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_component(blade, completed_blade)}
    return result
