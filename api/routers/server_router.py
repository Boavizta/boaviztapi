import copy

from fastapi import APIRouter

from api.DTO.server_DTO import Server, ServerDTO
from api.service.verbose import verbose_device
from api.service.bottom_up import bottom_up_device

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.post('/ref-data')
def server_impact_ref_data(server: Server):
    return None


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
