import copy

from fastapi import APIRouter

from api.model.components.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentMotherBoard, ComponentPowerSupply, ComponentRack, ComponentBlade
from api.service.bottom_up import bottom_up_component


component_router = APIRouter(
    prefix='/v1/component',
    tags=['component']
)


@component_router.post('/cpu')
def cpu_impact_bottom_up(cpu: ComponentCPU):
    enriched_cpu = copy.deepcopy(cpu)
    return bottom_up_component(component=enriched_cpu)


@component_router.post('/ram')
def ram_impact_bottom_up(ram: ComponentRAM):
    enriched_ram = copy.deepcopy(ram)
    return bottom_up_component(component=enriched_ram)


@component_router.post('/ssd')
def ssd_impact_bottom_up(ssd: ComponentSSD):
    enriched_ssd = copy.deepcopy(ssd)
    return bottom_up_component(component=enriched_ssd)


@component_router.post('/hdd')
def hdd_impact_bottom_up(hdd: ComponentHDD):
    enriched_hdd = copy.deepcopy(hdd)
    return bottom_up_component(component=enriched_hdd)


@component_router.post('/motherboard')
def motherboard_impact_bottom_up(motherboard: ComponentMotherBoard):
    enriched_motherboard = copy.deepcopy(motherboard)
    return bottom_up_component(component=enriched_motherboard)


@component_router.post('/power-supply')
def power_supply_impact_bottom_up(power_supply: ComponentPowerSupply):
    enriched_power_supply = copy.deepcopy(power_supply)
    return bottom_up_component(component=enriched_power_supply)


@component_router.post('/rack')
def rack_impact_bottom_up(rack: ComponentRack):
    enriched_rack = copy.deepcopy(rack)
    return bottom_up_component(component=enriched_rack)


@component_router.post('/blade')
def blade_impact_bottom_up(blade: ComponentBlade):
    enriched_blade = copy.deepcopy(blade)
    return bottom_up_component(component=enriched_blade)
