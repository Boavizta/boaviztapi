import copy

from fastapi import APIRouter

from api.dto.server_dto import ServerDTO
from api.service.archetype import find_archetype, get_server_archetype, complete_with_archetype, get_server_achetype_lst
from api.service.verbose import verbose_device
from api.service.bottom_up import bottom_up_device

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.get('/get_archetype')
def server_get_achetype(archetype: str):
    server = get_server_archetype(archetype)
    if not server:
        result = {"server_archtype": "Not found"}
    else:
        result = {"server_archtype": server}
    return result



@server_router.get('/all_archetype')
def server_get_all_achetype_name():
    return get_server_achetype_lst()



@server_router.post('/archetype')
def server_impact_ref_data(archetype: str, verbose: bool = True):
    server = get_server_archetype(archetype)
    completed_server = copy.deepcopy(server)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result


@server_router.post('/bottom-up')
def server_impact_bottom_up(server_dto: ServerDTO, verbose: bool = True):
    server = server_dto.to_device()
    completed_server = copy.deepcopy(server)

    if server.model.archetype:
        server_archetype = get_server_archetype(server.model.archetype)
        completed_server = complete_with_archetype(server_archetype, completed_server)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result
