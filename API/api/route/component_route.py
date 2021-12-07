import copy

from flask import Blueprint
from flask_pydantic import validate
from flask_pydantic_spec import Response


from API.api.model.components.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentMotherBoard, ComponentPowerSupply, ComponentRack, ComponentBlade
from API.api.service.bottom_up import bottom_up_component

component_api = Blueprint('component_api', __name__, url_prefix='/v1/component')


@component_api.route('/cpu', methods=['POST'])
@validate()
def cpu_impact_bottom_up(body: ComponentCPU):

    enriched_cpu = copy.deepcopy(body)

    return bottom_up_component(component=enriched_cpu)


@component_api.route('/ram', methods=['POST'])
@validate()
def ram_impact_bottom_up(body: ComponentRAM):

    enriched_ram = copy.deepcopy(body)

    return bottom_up_component(component=enriched_ram)


@component_api.route('/ssd', methods=['POST'])
@validate()
def ssd_impact_bottom_up(body: ComponentSSD):

    enriched_ssd = copy.deepcopy(body)

    return bottom_up_component(component=enriched_ssd)


@component_api.route('/hdd', methods=['POST'])
@validate()
def hdd_impact_bottom_up(body: ComponentHDD):

    enriched_hdd = copy.deepcopy(body)

    return bottom_up_component(component=enriched_hdd)


@component_api.route('/motherboard', methods=['POST'])
@validate()
def motherboard_impact_bottom_up(body: ComponentMotherBoard):

    enriched_motherboard = copy.deepcopy(body)

    return bottom_up_component(component=enriched_motherboard)


@component_api.route('/power-supply', methods=['POST'])
@validate()
def power_supply_impact_bottom_up(body: ComponentPowerSupply):

    enriched_power_supply = copy.deepcopy(body)

    return bottom_up_component(component=enriched_power_supply)


@component_api.route('/rack', methods=['POST'])
@validate()
def rack_impact_bottom_up(body: ComponentRack):

    enriched_rack = copy.deepcopy(body)

    return bottom_up_component(component=enriched_rack)


@component_api.route('/blade', methods=['POST'])
@validate()
def blade_impact_bottom_up(body: ComponentBlade):

    enriched_blade = copy.deepcopy(body)

    return bottom_up_component(component=enriched_blade)