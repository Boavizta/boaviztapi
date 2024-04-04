import requests
from shutil import copyfile
from csv import reader, writer
from pprint import pprint

AZURE_INSTANCES = "../../archetypes/cloud/azure.csv"
BOAVIZTAPI_BASE_URL = "https://api.boavizta.org/v1/cloud/"
BOAVIZTAPI_LOCAL_CONTAINER = "http://0.0.0.0:5000/v1"
RESULT_FILE = "result.csv"


query = {"provider": "azure", "verbose": "false"}

copyfile(AZURE_INSTANCES, RESULT_FILE)


def get_instance_gwp_impact_for_one_hour():

    with open(RESULT_FILE, "r") as result_file:
        result_reader = reader(result_file)
        data = list(result_reader)

    data[0].append("gwp_use_impact_one_hour")
    data[0].append("gwp_manufacturing_impact")
    data[0].append("energy_idle_1h")
    data[0].append("energy_50percent_1h")
    data[0].append("energy_100percent_1h")

    with open(AZURE_INSTANCES, "r") as azure_data:
        instances = azure_data.readlines()[1:]
        instance_gwp_use_impact_list = []
        instance_gwp_manufacturing_impact_list = []
        for instance in instances:
            instance_name = instance.split(",")[0]
            query.update({"instance_type": f"{instance_name}", "duration": 1, "criteria": "gwp"})
            impact_request = requests.get(
                f"{BOAVIZTAPI_LOCAL_CONTAINER}/cloud/instance", params=query
            )
            impact_json = impact_request.json()
            pprint(impact_json["impacts"]) 
            exit(1)
            instance_gwp_use_impact = impact_json["impacts"]["gwp"]["use"]["value"]
            instance_gwp_use_impact_list.append(instance_gwp_use_impact)
            instance_gwp_manufacturing_impact = impact_json["impacts"]["gwp"]["embedded"]["value"]
            instance_gwp_manufacturing_impact_list.append(instance_gwp_manufacturing_impact)

    for i in range(1, len(data)):
        data[i].append(instance_gwp_use_impact_list[i - 1])
        data[i].append(instance_gwp_manufacturing_impact_list[i - 1])

    with open(RESULT_FILE, "w") as result_file:
        result_writer = writer(result_file)
        result_writer.writerows(data)


get_instance_gwp_impact_for_one_hour()
