import ast
import csv
import os
from typing import Union

import pandas as pd

from boaviztapi import data_dir


def get_device_archetype_lst(path):
    df = pd.read_csv(path)
    return df['id'].tolist()


def get_device_archetype_lst_with_type(path, name: str, ) -> Union[dict, bool]:
    df = pd.read_csv(path)
    df = df[df['device_type'] == name]
    return df['id'].tolist()


def get_component_archetype(archetype_name: str, component_type: str) -> Union[dict, bool]:
    arch = get_archetype(archetype_name, os.path.join(data_dir, "archetypes/components/" + component_type + ".csv"))
    if not arch:
        return False
    return arch


def get_server_archetype(archetype_name: str) -> Union[dict, bool]:
    arch = get_archetype(archetype_name, os.path.join(data_dir, "archetypes/server.csv"))
    if not arch:
        return False
    return arch


def get_user_terminal_archetype(archetype_name: str) -> Union[dict, bool]:
    arch = get_archetype(archetype_name, os.path.join(data_dir, "archetypes/user_terminal.csv"))
    if not arch:
        return False
    return arch


def get_cloud_instance_archetype(archetype_name: str, provider: str) -> Union[dict, bool]:
    arch = False
    if os.path.exists(data_dir + "/archetypes/cloud/" + provider + ".csv"):
        arch = get_archetype(archetype_name, os.path.join(data_dir, "archetypes/cloud/" + provider + ".csv"))
    if not arch:
        return False
    return arch


def get_archetype(archetype_name: str, csv_path: str) -> Union[dict, bool]:
    reader = csv.DictReader(open(csv_path, encoding='utf-8'))
    for row in reader:
        if row["id"] == archetype_name:
            return row2json(row)
    return False


def parse_to_boattribute_json(value):
    json = {}
    if value == "" or value is None:
        return json
    elif ";" in value:
        values = value.split(";")
        if len(values) == 3:
            json["default"] = convert(values[0])
            json["min"] = convert(values[1])
            json["max"] = convert(values[2])
        if len(values) == 2:
            json["default"] = convert(values[0])
            if convert(values[1]) > convert(values[0]):
                json["min"] = convert(values[0])
                json["max"] = convert(values[1])
            else:
                json["min"] = convert(values[1])
                json["max"] = convert(values[0])
    else:
        json["default"] = convert(value)
    return json


def row2json(archetype):
    obj = {}
    for attribute in archetype:
        if attribute == "id":
            continue
        value = parse_to_boattribute_json(archetype[attribute])
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


def get_arch_value(archetype: dict, attribute: str, key: str, default=None):
    if not archetype:
        return default
    if archetype.get(attribute) is not None:
        if archetype.get(attribute).get(key) is not None:
            return archetype.get(attribute).get(key)
    return default


def get_arch_component(archetype: dict, component_name: str, default=None):
    if not archetype:
        return default
    if archetype.get(component_name) is not None:
        if component_name != "USAGE" and archetype.get("USAGE") is not None:
            archetype[component_name]["USAGE"] = archetype.get("USAGE")
        return archetype.get(component_name)
    return default


def get_iot_device_archetype(archetype_name: str) -> Union[dict, bool]:
    arch = get_archetype(archetype_name, os.path.join(data_dir, "archetypes/iot_device.csv"))
    if not arch:
        return False
    return arch

def convert(value):
    try:
        value_float = float(value)
        return value_float
    except ValueError:
        if "{" in value and "}" in value or "[" in value and "]" in value:
            try:
                value_dict = ast.literal_eval(value)
                if isinstance(value_dict, dict):
                    return value_dict
            except ValueError:
                pass

    return value