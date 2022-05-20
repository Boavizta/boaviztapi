import copy

from fastapi import APIRouter, Body

from boaviztapi.dto.component_dto import Cpu, Ram, Disk, PowerSupply, MotherBoard, Case
from boaviztapi.routers.openapi_doc.descriptions import cpu_description, ram_description, ssd_description, \
    hdd_description, motherboard_description, power_supply_description, case_description
from boaviztapi.routers.openapi_doc.examples import components_examples
from boaviztapi.service.bottom_up import bottom_up_component
from boaviztapi.service.verbose import verbose_component

consumption_profile = APIRouter(
    prefix='/v1/consumption_profile',
    tags=['consumption_profile']
)


@consumption_profile.post('/cpu',
                          description="cpu consumption profile generator")
async def cpu_consumption_profile(cpu: Cpu = Body(None, example=components_examples["cpu"]), verbose: bool = True):
    pass
