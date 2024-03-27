#!/usr/bin/python3

import pandas as pd

target_data = pd.DataFrame({
    "id": [],
    "manufacturer": [],
    "CASE.case_type": [],
    "CPU.units": [],
    "CPU.core_units": [],
    "CPU.die_size": [],
    "CPU.die_size_per_core": [],
    "CPU.tdp": [],
    "CPU.name": [],
    "CPU.vcpu": [],
    "RAM.units": [],
    "RAM.capacity": [],
    "SSD.units": [],
    "SSD.capacity": [],
    "HDD.units": [],
    "HDD.capacity": [],
    "GPU.units": [],
    "GPU.name": [],
    "GPU.memory_capacity": [],
    "POWER_SUPPLY.units": [],
    "POWER_SUPPLY.unit_weight": [],
    "USAGE.time_workload": [],
    "USAGE.use_time_ratio": [],
    "USAGE.hours_life_time": [],
    "USAGE.other_consumption_ratio": [],
    "WARNINGS": []
})

source_columns = ["Dedicated Host SKUs (VM series and Host Type)",
            "Available vCPUs","Available RAM","CPU",
            "Pay as you go"]

source_dedicated_hosts_file = "cleaned_dedicated_hosts.csv"
target_servers_file = "azure_servers.csv"

data = pd.read_csv(source_dedicated_hosts_file)

def compute_ram_sticks(ram_total_capacity):
    """
    Tries to guess how many RAM sticks are in a host containing
    ram_total_capacity and the associated memory capacity per stick.

    Strategy :
        - keep capacity per stick under 64 GB
        - keep nb_of_sticks below 64 as much as possible, first rule has priority

    returns

    0: nb_of_sticks, the number of RAM sticks
    1: stick_capacity, the capacity per RAM stick
    """
    ram_total_capacity = float(ram_total_capacity.replace(" GiB", "").replace(",", ""))
    stick_capacity = 8.0
    nb_of_sticks = ram_total_capacity / stick_capacity
    while nb_of_sticks > 64:
        if stick_capacity < 64:
            stick_capacity = stick_capacity * 2
        else:
            break;
        nb_of_sticks = ram_total_capacity / stick_capacity
    return nb_of_sticks, stick_capacity

for host in data[["Dedicated Host SKUs (VM series and Host Type)", "Available vCPUs","Available RAM","CPU"]].iterrows():
    print(host)
    nb_of_sticks, stick_capacity = compute_ram_sticks(host[1]["Available RAM"])
    new_data = pd.DataFrame({
        "id": [host[1]["Dedicated Host SKUs (VM series and Host Type)"]],
        "manufacturer": ["Azure"],
        "CASE.case_type": [""],
        "CPU.units": [""],
        "CPU.core_units": [""],
        "CPU.die_size": [""],
        "CPU.die_size_per_core": [""],
        "CPU.tdp": [""],
        "CPU.name": [host[1]["CPU"]],
        "CPU.vcpu": [host[1]["Available vCPUs"]],
        "RAM.units": [nb_of_sticks],
        "RAM.capacity": [stick_capacity],
        "SSD.units": [""],
        "SSD.capacity": [""],
        "HDD.units": [""],
        "HDD.capacity": [""],
        "GPU.units": [""],
        "GPU.name": [""],
        "GPU.memory_capacity": [""],
        "POWER_SUPPLY.units": [""],
        "POWER_SUPPLY.unit_weight": [""],
        "USAGE.time_workload": [""],
        "USAGE.use_time_ratio": [""],
        "USAGE.hours_life_time": [""],
        "USAGE.other_consumption_ratio": [""],
        "WARNINGS": ["RAM capacity from Azure docs : {}".format(host[1]["Available RAM"])]
    })
    target_data = pd.concat([target_data, new_data])

target_data.to_csv(target_servers_file, index=False)