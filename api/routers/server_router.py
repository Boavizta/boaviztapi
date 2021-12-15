import copy

from fastapi import APIRouter

from api.model.devices.server import Server
from api.service.verbose import verbose_components
from api.service.bottom_up import bottom_up_components
from api.service.server_impact.ref.ref import ref_data_server

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.post('/ref-data')
def server_impact_ref_data(server: Server):
    impacts = ref_data_server(server)
    return impacts


@server_router.post('/bottom-up')
def server_impact_bottom_up(server: Server, verbose: bool = True):
    components = server.get_component_list()
    completed_components = copy.deepcopy(components)

    impacts = bottom_up_components(components=completed_components)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_components(components, completed_components)}

    return result
