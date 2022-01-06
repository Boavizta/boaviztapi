import os

from api.dto.server_dto import ServerDTO
from api.model.devices.device import Server, Device

server_directory = './data/devices/server'
servers = []


def get_server_archetype(archtype_name: str) -> Server:
    pass


def complete_with_archetype(server: Server, archetype_server: Server) -> Server:
    pass


def find_archetype(server_dto: ServerDTO) -> Server:
    """
    TODO issue #1 find server by name, year, brand, ...
        replace the configuration variable sent by the user
        return server
    """
