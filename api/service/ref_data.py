from api.dto.server_dto import ServerDTO
from api.model.devices.device import Server


def ref_server(server_dto: ServerDTO) -> Server:

    return server_dto.to_device()
