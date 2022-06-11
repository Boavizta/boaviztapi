import copy
import os
from typing import Type

from fastapi import APIRouter, Body, Query

from boaviztapi.dto.device import DeviceDTO, Server
from boaviztapi.model.device import Device, DeviceServer
from boaviztapi.routers import data_dir
from boaviztapi.routers.openapi_doc.descriptions import server_impact_by_model_description, \
    all_default_model_description, server_impact_by_config_description
from boaviztapi.routers.openapi_doc.examples import server_configuration_examples
from boaviztapi.service.archetype import get_server_archetype, complete_with_archetype, \
    get_device_archetype_lst
from boaviztapi.service.verbose import verbose_device
from boaviztapi.service.bottom_up import bottom_up_device

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


# @server_router.get('/model',
#                    description=server_impact_by_model_description)
# async def server_impact_by_model(archetype: str = Query(None, example="dellR740"), verbose: bool = True):
#     server = await get_server_archetype(archetype)
#     completed_server = copy.deepcopy(server)
#
#     impacts = bottom_up_device(device=completed_server)
#     result = impacts
#
#     if verbose:
#         result = {"impacts": impacts,
#                   "verbose": verbose_device(complete_device=completed_server, input_device=server)}
#
#     return result


@server_router.get('/all_default_models',
                   description=all_default_model_description)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/server'))


@server_router.get('/model',
                   description=server_impact_by_model_description)
async def server_impact_from_model(archetype: str = Query(None, example="dellR740"), verbose: bool = True):
    raise NotImplementedError


@server_router.post('/',
                    description=server_impact_by_config_description)
async def server_impact_from_configuration(
        server: Server = Body(None, example=server_configuration_examples["DellR740"]),
        verbose: bool = True
):
    # TODO: Reimplement archetype with Server (DTO) object
    # if server.model.archetype:
    #     server_archetype = await get_server_archetype(server.model.archetype)
    #     completed_server = complete_with_archetype(completed_server, server_archetype)
    completed_server = server.copy()
    return await server_impact(
        input_device_dto=server,
        smart_complete_device_dto=completed_server,
        device_class=DeviceServer,
        verbose=verbose
    )


async def server_impact(input_device_dto: DeviceDTO,
                        smart_complete_device_dto: DeviceDTO,
                        device_class: Type[Device],
                        verbose: bool) -> dict:
    device = device_class.from_dto(smart_complete_device_dto)
    impacts = bottom_up_device(device=device)
    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(input_device_dto=input_device_dto,
                                      output_device_dto=device.to_dto(smart_complete_device_dto))
        }
    return impacts
