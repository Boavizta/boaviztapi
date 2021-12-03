import json
from copy import copy

from flask import Blueprint, request
from flask_pydantic import validate

from api.model.server import Server
from api.service.server_impact.bottom_up.bottom_up import bottom_up_server
from api.service.server_impact.ref.ref import ref_data_server

server_api = Blueprint('server_api', __name__, url_prefix='/v1/server')


@server_api.route('/ref_data', methods=['POST'])
@validate()
def server_impact_ref_data(body: Server):
    # TODO: returns the closest server impact in the referenced data of Boavizta
    # server = server_mapper(request.json)
    #impacts = ref_data_server(server).to_json()
    print("\n\n Method : ref data \n\n")
    impacts = ref_data_server(body)
    return impacts


@server_api.route('/bottom-up', methods=['POST'])
@validate()
def server_impact_bottom_up(body: Server):
    input_ = copy(body)
    server_impacts = bottom_up_server(body)
    return format_output(input_, server_impacts)
    # return {'impacts': impacts, 'enriched_data': server_impacts.dict()}


@server_api.route('/', methods=['POST'])
def server_impact_auto():
    # TODO: returns the server impact with the best methodology
    return {}
