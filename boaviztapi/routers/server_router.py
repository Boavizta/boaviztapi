import copy

from fastapi import APIRouter

from boaviztapi.dto.server_dto import ServerDTO
from boaviztapi.service.archetype import get_server_archetype, get_server_archetype_lst, complete_with_archetype
from boaviztapi.service.verbose import verbose_device
from boaviztapi.service.bottom_up import bottom_up_device

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.get('/model',
                   description="Get the impact of a server by the model name given in parameter")
def server_impact_ref_data(archetype: str, verbose: bool = True):
    server = get_server_archetype(archetype)
    completed_server = copy.deepcopy(server)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result


@server_router.post('/',
                    description="Default route, return the impact of a given Server")
def server_impact_bottom_up(server_dto: ServerDTO, verbose: bool = True):
    server = server_dto.to_device()
    completed_server = copy.deepcopy(server)

    if server.model.archetype:
        server_archetype = get_server_archetype(server.model.archetype)
        completed_server = complete_with_archetype(
            completed_server, server_archetype)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result


"""
@server_router.get('/get_archetype',
                   description="Return the description of an archetype given in parameter")
def server_get_archetype(archetype: str):
    server = get_server_archetype(archetype)
    if not server:
        result = {"server_archetype": "Not found"}
    else:
        result = {"server_archetype": server}
    return result
"""


@server_router.get('/all_default_models',
                   description="Get the name of all available servers with a known configuration")
def server_get_all_archetype_name():
    return get_server_archetype_lst()
