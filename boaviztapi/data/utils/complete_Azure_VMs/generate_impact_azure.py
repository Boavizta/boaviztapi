import requests
from shutil import copyfile
from csv import reader, writer

AZURE_INSTANCES = "../../archetypes/cloud/azure.csv"
BOAVIZTAPI_BASE_URL = "https://api.boavizta.org/v1/cloud/"
BOAVIZTAPI_LOCAL_CONTAINER = "http://0.0.0.0:5000/v1"
RESULT_FILE = "../../archetypes/cloud/result.csv"


query = {"provider": "azure", "verbose": "false"}

copyfile(AZURE_INSTANCES, RESULT_FILE)


def get_instance_gwp_impact_for_one_hour():

    with open(RESULT_FILE, "r") as result_file:
        result_reader = reader(result_file)
        data = list(result_reader)

    data[0].append("gwp_use_impact_one_hour")

    with open(AZURE_INSTANCES, "r") as azure_data:
        instances = azure_data.readlines()[1:]
        instance_impact_list = []
        for instance in instances:
            instance_name = instance.split(",")[0]
            query.update({"instance_type": f"{instance_name}", "duration": 1, "criteria": "gwp"})
            impact_request = requests.get(
                f"{BOAVIZTAPI_LOCAL_CONTAINER}/cloud/instance", params=query
            )
            impact_json = impact_request.json()
            instance_impact = impact_json["impacts"]["gwp"]["use"]["value"]
            instance_impact_list.append(instance_impact)

    for impact in range(1, len(data)):
        data[impact].append(instance_impact_list[impact - 1])

    with open(RESULT_FILE, "w") as result_file:
        result_writer = writer(result_file)
        result_writer.writerows(data)


get_instance_gwp_impact_for_one_hour()
