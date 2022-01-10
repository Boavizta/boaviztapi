import os
from typing import List

from api.dto.server_dto import ServerDTO
from api.model.devices.device import Server, Device
import json
import os
known_server_directory = './data/devices/server'

# for the name of the variables : known or profil or archetype
servers = []


def get_server_achetype_lst() -> list:
    known_devices_lst = os.listdir(known_server_directory)
    return [file_name.split(".")[0] for file_name in known_devices_lst] 

def get_server_archetype(archtype_name: str) -> Server:
    known_devices_lst = get_server_achetype_lst()
    for device_name in known_devices_lst:
        if archtype_name == device_name:
            known_server = ServerDTO.parse_file(known_server_directory + '/' + device_name + ".json")
            return known_server
    return False


def complete_with_archetype(server: Server, archetype_server: Server) -> Server:
    pass


def find_archetype(server_dto: ServerDTO) -> Server:
    """
    TODO issue #1 find server by name, year, brand, ...
        replace the configuration variable sent by the user
        return server
    """
