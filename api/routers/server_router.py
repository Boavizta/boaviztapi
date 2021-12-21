import copy

from fastapi import APIRouter

from api.dto.server_dto import ServerDTO
from api.service.verbose import verbose_device
from api.service.bottom_up import bottom_up_device
from api.service.ref_data import ref_server

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.post('/ref-data')
def server_impact_ref_data(client_server_dto: ServerDTO, verbose: bool = True):
    server = ref_server(server_dto=client_server_dto)

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

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result
