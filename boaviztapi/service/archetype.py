from typing import Union
from pathlib import Path

from boaviztapi.dto.server_dto import ServerDTO, CloudDTO
from boaviztapi.model.devices.device import Server, Device, CloudInstance

import os

from boaviztapi.service import data_dir

known_server_directory = os.path.join(data_dir, 'devices/server')
known_instances_directory = os.path.join(data_dir, 'devices/cloud')


def get_device_archetype_lst(path=known_server_directory) -> list:
    known_devices_lst = os.listdir(path)
    return [Path(file_name).stem for file_name in known_devices_lst]


def complete_with_archetype(device: Device, archetype_device: Device) -> Device:
    # TODO: this method should have a recursive way of treating attribute for complex attribute (object and dictionary)
    """
    set the missing server components of server from its archetype
    """
    lst_id = set()
    for component in device.config_components:
        for i, component_to_remove in enumerate(archetype_device.config_components):
            if component.TYPE == component_to_remove.TYPE:
                lst_id.add(i)

    for index in sorted(list(lst_id), reverse=True):
        del archetype_device.config_components[index]
    archetype_device.config_components += device.config_components

    for attr, value in device.usage.__iter__():
        if attr != "TYPE" and attr != "hash":
            if type(value) is dict:
                setattr(archetype_device.usage, attr, recursive_dict_complete(value,
                                                                              getattr(archetype_device.usage, attr)))
            elif value is not None:
                setattr(archetype_device.usage, attr, value)

    return archetype_device


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
            known_server = ServerDTO.parse_file(
                path + '/' + device_name + ".json").to_device()
            return known_server
    return False


def get_cloud_instance_archetype(archetype_name: str, provider, path=known_instances_directory) \
        -> Union[CloudInstance, bool]:
    known_cloud_instance_lst = get_device_archetype_lst(os.path.join(path, provider))
    for device_name in known_cloud_instance_lst:
        if archetype_name == device_name:
            known_server = CloudDTO.parse_file(
                path + '/' + provider + '/' + device_name + ".json").to_device()
            return known_server
    return False


def find_archetype(server_dto: ServerDTO) -> Server:
    """
    TODO find the closer archetype by name, year, brand, config, ..
    """
