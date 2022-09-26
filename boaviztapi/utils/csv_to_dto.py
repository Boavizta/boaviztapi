import csv
import json


def make_dto(csv_file_path, json_path):
    csv_reader = csv.DictReader(open(csv_file_path, encoding='utf-8'))

    for rows in csv_reader:
        obj = {}
        json_file = open(json_path + "/" + rows["model.name"] + ".json", 'w', encoding='utf-8')
        for attribute in rows:
            value = rows[attribute]
            if value == "" or value is None:
                continue
            names = attribute.split('.')
            nested_set(obj, names, value)
        obj = set_list(obj)
        json_file.write(json.dumps(obj))


# Get a given data from a dictionary with position provided as a list
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


_csv_file_path = '../data/devices/cloud/source/EC2 Instances Carbon Footprint Estimator TEADS.csv'
_json_path = '../data/devices/cloud/aws'

if __name__ == '__main__':
    make_dto(_csv_file_path, _json_path)
