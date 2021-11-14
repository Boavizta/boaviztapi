from flask import Blueprint

server_api = Blueprint('server_impacts', __name__, url_prefix='/server')


@server_api.route('/v1/server/ref-data')
def server_impact_ref_data():
    # TODO: returns the closest server impact in the referenced data of Boavizta
    return {}


@server_api.route('/v1/server/bottom-up')
def server_impact_bottom_up():
    # TODO: returns the server impact with the bottom-up methodology
    return {}


@server_api.route('/v1/server')
def server_impact_auto():
    # TODO: returns the server impact with the best methodology
    return {}
