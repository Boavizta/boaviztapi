from typing import Union

from boaviztapi.dto.server_dto import ServerDTO
from boaviztapi.model.devices.device import Server
import os

known_server_directory = './data/devices/server'

# for the name of the variables : known || profile || archetype
servers = []


def get_server_archetype_lst() -> list:
    known_devices_lst = os.listdir(known_server_directory)
    return [file_name.split(".")[0] for file_name in known_devices_lst]


def get_server_archetype(archetype_name: str) -> Union[Server, bool]:
    known_devices_lst = get_server_archetype_lst()
    for device_name in known_devices_lst:
        if archetype_name == device_name:
            known_server = ServerDTO.parse_file(
                known_server_directory + '/' + device_name + ".json").to_device()
            return known_server
    return False


def complete_with_archetype(server: Server, archetype_server: Server) -> Server:
    """
    TODO #1
    set the missing server components of server from its archetype
    ? set the missing attributes of components ?
    """
    lst_id = set()
    for component in server.config_components:
        for i, component_to_remove in enumerate(archetype_server.config_components):
            if component.TYPE == component_to_remove.TYPE:
                lst_id.add(i)
    for index in sorted(list(lst_id), reverse=True):
        del archetype_server.config_components[index]
    archetype_server.config_components += server.config_components

    return archetype_server


def find_archetype(server_dto: ServerDTO) -> Server:
    """
    TODO find the closer archetype by name, year, brand, config, ..
    """
