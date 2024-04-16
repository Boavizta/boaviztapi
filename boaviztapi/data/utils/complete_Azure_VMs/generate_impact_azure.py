#!/usr/bin/env python3

import requests
from shutil import copyfile
from csv import reader, writer
from pprint import pprint
import json
import pandas as pd
import os

def clear():
    """
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    """
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')
    
AWS_INSTANCES = "../../archetypes/cloud/aws.csv"
AZURE_INSTANCES = "../../archetypes/cloud/azure.csv"
BOAVIZTAPI_BASE_URL = "https://api.boavizta.org/v1/cloud/"
BOAVIZTAPI_LOCAL_CONTAINER = "http://0.0.0.0:5000/v1"
RESULT_FILE = "result.csv"
if "GEN_IMPACT_PROVIDER" in os.environ and os.environ["GEN_IMPACT_PROVIDER"] == "aws":
    RESULT_FILE = "aws_result.csv"

if "GEN_IMPACT_PROVIDER" in os.environ and os.environ["GEN_IMPACT_PROVIDER"] == "aws":
    base_data = pd.read_csv(AWS_INSTANCES)
else:
    base_data = pd.read_csv(AZURE_INSTANCES)

def get_instance_impact(instance_name, usage_hours, usage_location, load_percentage):
    """Returns impacts json object for `instance_name`, by querying the BoaviztAPI located at BOAVIZTAPI_LOCAL_CONTAINER.

    Keyword arguments:
    instance_name -- str, the name/id of the instance
    usage_hours -- int, how many hours of runtime should be considered to compute impacts
    usage_location -- str, three-letters code identifying the country and electricity mix for runtime, see columns in https://github.com/Boavizta/boaviztapi/blob/main/boaviztapi/data/crowdsourcing/electrical_mix.csv
    load_percentage -- int, what average percentage of CPU time usage should be considered for impacts calculation
    """
    provider = "azure"
    if "GEN_IMPACT_PROVIDER" in os.environ and os.environ["GEN_IMPACT_PROVIDER"] == "aws":
        provider = "aws"
    if usage_hours > 0:
        query = {"provider": provider, "verbose": "true", "duration": usage_hours}
    else:
        query = {"provider": provider, "verbose": "true"}
    data = {
      "provider": provider,
      "instance_type": f"{instance_name}",
      "verbose": "true",
      "usage": {
        "usage_location": f"{usage_location}",
        "time_workload": [
          {
            "time_percentage": 100,
            "load_percentage": f"{load_percentage}"
          }
        ]
      }
    }
    impact_request = requests.post(
        f"{BOAVIZTAPI_LOCAL_CONTAINER}/cloud/instance",
        data=json.dumps(data),
        params=query
    )
    return impact_request.json()

def make_instance_impacts():
    """
    Reads AZURE_INSTANCES file, adds columns for impact, writes RESULT_FILE.
    """
    usage_locations = ["FRA", "GBR", "USA"] 
    load_averages = [0, 50, 100]

    final_data = pd.concat(
        [base_data, pd.DataFrame({
            "gwp_manufacturing_1h_impact": [],
            "gwp_manufacturing_total_host_lifetime_impact": []
        })], axis=1
    )
    for load in load_averages:
        final_data = pd.concat(
            [final_data,
            pd.DataFrame({
                "energy_1h_load{}".format(load): []
            })], axis=1
        )
        for location in usage_locations:
            final_data = pd.concat(
                [final_data, 
                pd.DataFrame({
                    "gwp_use_1h_load{}_{}".format(load, location): [],
                })], axis=1
            )
    
    for instance in base_data[["id"]].iterrows():
        clear()
        completion_percentage = round(instance[0] / len(base_data.index) * 100.0, 1)
        print("Building data... {}%".format(completion_percentage))
        instance_name = instance[1]["id"].split(",")[0]
        if completion_percentage > 50:
            final_data.to_csv(RESULT_FILE)
        impacts = {}
        impacts_total_lifetime = get_instance_impact(instance_name, -1, "GBR", 0)
        for location in usage_locations:
            impacts[location] = {}
            for load in load_averages:
                impacts[location][load] = get_instance_impact(instance_name, 1, location, load)
                final_data["gwp_use_1h_load{}_{}".format(load, location)].values[instance[0]] = impacts[location][load]["impacts"]["gwp"]["use"]["value"]
        for load in load_averages:
            final_data["energy_1h_load{}".format(load)].values[instance[0]] = impacts[usage_locations[0]][load]["verbose"]["avg_power"]["value"]
        final_data["gwp_manufacturing_1h_impact"].values[instance[0]] = impacts[usage_locations[0]][load_averages[0]]["impacts"]["gwp"]["embedded"]["value"]
        final_data["gwp_manufacturing_total_host_lifetime_impact"].values[instance[0]] = impacts_total_lifetime["impacts"]["gwp"]["embedded"]["value"]


    final_data.to_csv(RESULT_FILE, index=False)
    print("Results written in {}".format(RESULT_FILE))

if __name__ == "__main__":
    make_instance_impacts()
