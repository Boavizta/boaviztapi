import csv
import os
from typing import Union

import pandas as pd

from boaviztapi.dto.device import Server, Cloud, DeviceDTO
from boaviztapi.service import data_dir


def get_device_archetype_lst(path):
    df = pd.read_csv(path)
    return df['model.name'].tolist()


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


async def get_server_archetype(archetype_name: str) -> Union[Server, bool]:
    arch = get_archetype(archetype_name, os.path.join(data_dir, "devices/server/server.csv"))
    if not arch:
        return False
    return Server.parse_obj(arch)


async def get_cloud_instance_archetype(archetype_name: str, provider: str) -> Union[Cloud, bool]:
    arch = False
    if os.path.exists(data_dir+"/devices/cloud/"+provider+".csv"):
        arch = get_archetype(archetype_name, os.path.join(data_dir, "devices/cloud/"+provider+".csv"))
    if not arch:
        return False
    return Cloud.parse_obj(arch)


def get_archetype(archetype_name: str, csv_path: str) -> Union[dict, bool]:
    reader = csv.DictReader(open(csv_path, encoding='utf-8'))
    for row in reader:
        if row["model.name"] == archetype_name:
            print(row2json(row))
            return row2json(row)
    return False


def row2json(archetype):
    obj = {}
    for attribute in archetype:
        value = archetype[attribute]
        if value == "" or value is None:
            continue
        names = attribute.split('.')
        nested_set(obj, names, value)
    obj = set_list(obj)
    return obj


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def set_list(obj):
    if obj.get("configuration") is not None:
        if obj.get("configuration").get("disk"):
            obj["configuration"]["disk"] = [obj["configuration"]["disk"]]
        if obj.get("configuration").get("ram"):
            obj["configuration"]["ram"] = [obj["configuration"]["ram"]]
    return obj


def find_archetype(server_dto: Server) -> Server:
    """
    TODO find the closer archetype by name, year, brand, config, ..
    """
    pass
