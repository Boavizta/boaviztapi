import copy

from flask import Blueprint
from flask_pydantic import validate

from API.api.model.devices.server import Server
from API.api.service.bottom_up import bottom_up_components
from API.api.service.server_impact.ref.ref import ref_data_server

server_api = Blueprint('server_api', __name__, url_prefix='/v1/server')


@server_api.route('/ref_data', methods=['POST'])
@validate()
def server_impact_ref_data(body: Server):
    # TODO: returns the closest server impact in the referenced data of Boavizta
    # server = server_mapper(request.json)
    # impacts = ref_data_server(server).to_json()
    print("\n\n Method : ref data \n\n")
    impacts = ref_data_server(body)
    return impacts


@server_api.route('/bottom-up', methods=['POST'])
@validate()
def server_impact_bottom_up(body: Server):
    components = body.get_component_list()
    enriched_components = copy.deepcopy(components)
    return bottom_up_components(components=enriched_components)
