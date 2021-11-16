from flask import Blueprint, request

from api.model.server import server_mapper
from api.service.server_impact.bottom_up.bottom_up import bottom_up_server

server_api = Blueprint('server_api', __name__, url_prefix='/v1/server')


@server_api.route('/ref-data')
def server_impact_ref_data():
    # TODO: returns the closest server impact in the referenced data of Boavizta
    return {}


@server_api.route('/bottom-up', methods=['POST'])
def server_impact_bottom_up():
    # create server object
    server = server_mapper(request.json)
    # apply bottom_up methodology
    res = bottom_up_server(server)
    return res


@server_api.route('/')
def server_impact_auto():
    # TODO: returns the server impact with the best methodology
    return {}
