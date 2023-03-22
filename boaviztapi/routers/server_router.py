import os

from fastapi import APIRouter, Body, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device import Server
from boaviztapi.dto.device.device import mapper_server
from boaviztapi.model.device import Device, DeviceServer
from boaviztapi.routers.openapi_doc.descriptions import server_impact_by_model_description, \
    all_default_model_description, server_impact_by_config_description
from boaviztapi.routers.openapi_doc.examples import server_configuration_examples
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.archetype import get_server_archetype, get_device_archetype_lst
from boaviztapi.service.verbose import verbose_device
from boaviztapi.service.bottom_up import bottom_up

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.get('/all_default_models',
                   description=all_default_model_description)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'archetypes/server.csv'))


@server_router.get('/model',
                   description=server_impact_by_model_description)
async def server_impact_from_model(archetype: str = config["default_server"], verbose: bool = True,
                                   allocation: Allocation = Allocation.TOTAL):
    archetype_config = get_server_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    model_server=DeviceServer(archetype=archetype_config)

    return await server_impact(
        device=model_server,
        verbose=verbose,
        allocation=allocation
    )


@server_router.post('/',
                    description=server_impact_by_config_description)
async def server_impact_from_configuration(
        server: Server = Body(None, example=server_configuration_examples["DellR740"]),
        verbose: bool = True, allocation: Allocation = Allocation.TOTAL, archetype: str = config["default_server"]):

    archetype_config = get_server_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    completed_server = mapper_server(server, archetype=archetype_config)

    return await server_impact(
        device=completed_server,
        verbose=verbose,
        allocation=allocation
    )

async def server_impact(device: Device,
                        verbose: bool, allocation: Allocation) -> dict:
    impacts = bottom_up(model=device, allocation=allocation)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(device)
        }
    return impacts