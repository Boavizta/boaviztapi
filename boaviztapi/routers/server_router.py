import copy
import os

from fastapi import APIRouter, Body, Query

from boaviztapi.dto.server_dto import ServerDTO
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


@server_router.get('/model',
                   description=server_impact_by_model_description)
async def server_impact_by_model(archetype: str = Query(None, example="dellR740"), verbose: bool = True):
    server = await get_server_archetype(archetype)
    completed_server = copy.deepcopy(server)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result


@server_router.post('/bottom-up',
                    description="LEGACY ROUTE NAME for *Server Impact By Config* ")
@server_router.post('/',
                    description=server_impact_by_config_description)
async def server_impact_by_config(server_dto: ServerDTO = Body(None, example=server_configuration_examples["DellR740"]),
                                  verbose: bool = True):
    server = server_dto.to_device()
    completed_server = copy.deepcopy(server)

    if server.model.archetype:
        server_archetype = await get_server_archetype(server.model.archetype)
        completed_server = complete_with_archetype(
            completed_server, server_archetype)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result


@server_router.get('/all_default_models',
                   description=all_default_model_description)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/server'))
