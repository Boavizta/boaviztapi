import os
from pathlib import Path
from typing import Union

from boaviztapi.dto.device import Server, Cloud, DeviceDTO
from boaviztapi.service import data_dir

known_server_directory = os.path.join(data_dir, 'devices/server')
known_instances_directory = os.path.join(data_dir, 'devices/cloud')


def get_device_archetype_lst(path=known_server_directory) -> list:
    known_devices_lst = os.listdir(path)
    return [Path(file_name).stem for file_name in known_devices_lst]


def complete_with_archetype(device: DeviceDTO, archetype_device: DeviceDTO) -> dict:
    # TODO: this method should have a recursive way of treating attribute for complex attribute (object and dictionary)
    archetype_dict = recursive_dict_complete(device.dict(), archetype_device.dict())
    return archetype_dict


def recursive_dict_complete(dict1, dict2):
    for attr, value in dict1.items():
        if type(value) is dict:
            dict2[attr] = recursive_dict_complete(value, dict2[attr])
        elif value is not None:
            dict2[attr] = value
    return dict2


async def get_server_archetype(archetype_name: str, path=known_server_directory) -> Union[Server, bool]:
    known_server_lst = get_device_archetype_lst(path=path)
    for device_name in known_server_lst:
        if archetype_name == device_name:
            known_server = Server.parse_file(
                path + '/' + device_name + ".json")
            return known_server
    return False


async def get_cloud_instance_archetype(archetype_name: str, provider, path=known_instances_directory) \
        -> Union[Cloud, bool]:
    known_cloud_instance_lst = get_device_archetype_lst(os.path.join(path, provider))
    for device_name in known_cloud_instance_lst:
        if archetype_name == device_name:
            known_server = Cloud.parse_file(
                path + '/' + provider + '/' + device_name + ".json")
            return known_server
    return False


def find_archetype(server_dto: Server) -> Server:
    """
    TODO find the closer archetype by name, year, brand, config, ..
    """
    pass
