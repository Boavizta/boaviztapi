import copy
import json
import os
from typing import Type

from fastapi import APIRouter, Body, Query, HTTPException

from boaviztapi.dto.device import DeviceDTO, Server
from boaviztapi.dto.device.device import smart_mapper_server
from boaviztapi.model.device import Device, DeviceServer
from boaviztapi.routers import data_dir
from boaviztapi.routers.openapi_doc.descriptions import server_impact_by_model_description, \
    all_default_model_description, server_impact_by_config_description
from boaviztapi.routers.openapi_doc.examples import server_configuration_examples
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.archetype import get_server_archetype, complete_with_archetype, \
    get_device_archetype_lst
from boaviztapi.service.verbose import verbose_device
from boaviztapi.service.bottom_up import bottom_up_device

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.get('/all_default_models',
                   description=all_default_model_description)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/server'))


@server_router.get('/model',
                   description=server_impact_by_model_description)
async def server_impact_from_model(archetype: str = Query(None, example="dellR740"), verbose: bool = True,
                                   allocation: Allocation = Allocation.TOTAL):
    server = Server()
    server_archetype = await get_server_archetype(archetype)

    if not server_archetype:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    server_archetyped = Server(**complete_with_archetype(server, server_archetype))
    completed_server = smart_mapper_server(server_archetyped)

    return await server_impact(
        device=completed_server,
        verbose=verbose,
        allocation=allocation
    )


@server_router.post('/',
                    description=server_impact_by_config_description)
async def server_impact_from_configuration(
        server: Server = Body(None, example=server_configuration_examples["DellR740"]),
        verbose: bool = True, allocation: Allocation = Allocation.TOTAL):

    if server.model is not None and server.model.archetype is not None:
        server_archetype = await get_server_archetype(server.model.archetype)
        if server_archetype:
            server = Server(**complete_with_archetype(server, server_archetype))

    completed_server = smart_mapper_server(server)

    return await server_impact(
        device=completed_server,
        verbose=verbose,
        allocation=allocation
    )


async def server_impact(device: Device,
                        verbose: bool, allocation: Allocation) -> dict:
    impacts = bottom_up_device(device=device, allocation=allocation)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(device)
        }
    return impacts
