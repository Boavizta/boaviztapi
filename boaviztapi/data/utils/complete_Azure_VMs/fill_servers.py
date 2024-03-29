#!/usr/bin/python3

import pandas as pd
import re

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
source_cpu_spec_file = "../../crowdsourcing/cpu_specs.csv"
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

def get_cpu_spec(cpu_specs, cpu_ref_string):
    cpu_ref_string = re.sub(r"(\w+) Generation ", '', cpu_ref_string)
    cpu_ref_string = re.sub(r"([0-9]+\.[0-9]+) (GHz|Ghz) ", '', cpu_ref_string)
    cpu_ref_string = re.sub(r" (\(\w+\)).*", '', cpu_ref_string)
    cpu_ref_string = cpu_ref_string.replace("Scalable Processor", "Platinum")
    #exp = r"(AMD|Intel|Ampere)( Xeon|EPYC|Epyc)( Platinum|Gold|Silver|Bronze|Scalable)( [0-9]+\w*(-)?\w*)"
    #print("parsing {}".format(cpu_ref_string))
    #res = re.finditer(exp, cpu_ref_string)
    spec = None
    #if res is not None:
    #    for match in res:
    #        print("parsing {} gives: {}".format(cpu_ref_string, match))
    for s in cpu_specs[["name", "code_name", "generation", "manufacturer", "foundry", "manufacturer", "release_date", "frequency", "tdp", "cores", "threads", "process_size", "die_size", "io_die_size", "io_process_size", "total_die_size", "model_range"]].iterrows():
        if cpu_ref_string in s[1]["name"] or s[1]["name"] in cpu_ref_string or s[1]["name"].replace(" Xeon", "") in cpu_ref_string.replace("v", "V"):
            spec = s[1]
    return spec

def get_gpu_from_string(cpu_gpu_string):
    exp = re.compile("(AMD|NVIDIA).?.?.? (Radeon|Tesla) (\w+)?( (\w+)?(-)?(\w)*)? (GPUs)?")
    res = exp.search(cpu_gpu_string)
    if res is not None:
        return res.group().replace("GPUs", "")
    else:
        return None

def get_cpu_units(host_data, cpu_data):
    if cpu_data["threads"] != "nan":
        guessed_value = round(host_data["Available vCPUs"] / cpu_data["threads"])
        # sometimes the ratio is weird, sanity check required
        if guessed_value == 0:
            guessed_value = 1
        elif guessed_value == 7:
            guessed_value = 8
        elif guessed_value == 3:
            guessed_value = 4
        return guessed_value
    else:
        return None

cpu_specs = pd.read_csv(source_cpu_spec_file)

for host in data[["Dedicated Host SKUs (VM series and Host Type)", "Available vCPUs","Available RAM","CPU"]].iterrows():
    #print(host)
    current_cpu_spec = get_cpu_spec(cpu_specs, host[1]["CPU"])
    if current_cpu_spec is None:
        print("No spec found for: {}".format(host[1]["CPU"]))
    else:
        print("CPU: {} threads: {} host max vCPU : {} supposed CPU units: {}".format(current_cpu_spec["name"], current_cpu_spec["threads"], host[1]["Available vCPUs"], get_cpu_units(host[1], current_cpu_spec)))
    current_gpu = get_gpu_from_string(host[1]["CPU"])
    if current_gpu is not None:
        print("Current GPU: {}".format(current_gpu))
    nb_of_sticks, stick_capacity = compute_ram_sticks(host[1]["Available RAM"])
    new_data = pd.DataFrame({
        "id": [host[1]["Dedicated Host SKUs (VM series and Host Type)"]],
        "manufacturer": ["Azure"],
        "CASE.case_type": ["rack"], # TODO: source from Azure docs which platform is blade, which is rack
        "CPU.units": [get_cpu_units(host[1], current_cpu_spec)],
        "CPU.core_units": [""],
        "CPU.die_size": [""],
        "CPU.die_size_per_core": [""],
        "CPU.tdp": [current_cpu_spec["tdp"] if current_cpu_spec is not None else ""],
        "CPU.name": [host[1]["CPU"]],
        "CPU.vcpu": [host[1]["Available vCPUs"]],
        "RAM.units": [nb_of_sticks],
        "RAM.capacity": [stick_capacity],
        "SSD.units": [""],
        "SSD.capacity": [""],
        "HDD.units": [""],
        "HDD.capacity": [""],
        "GPU.units": [1], # TODO: guess it from how many GPUs have the biggest instances hosted on this platform
        "GPU.name": [current_gpu],
        "GPU.memory_capacity": [""],
        "POWER_SUPPLY.units": ["2;2;2"], # TODO: source from Azure docs which platform is blade, which is rack
        "POWER_SUPPLY.unit_weight": ["2.99;1;5"], # TODO: source from Azure docs which platform is blade, which is rack
        "USAGE.time_workload": [""],
        "USAGE.use_time_ratio": [""],
        "USAGE.hours_life_time": [""],
        "USAGE.other_consumption_ratio": [""],
        "WARNINGS": ["RAM units and per unit capacity not verified. RAM capacity from Azure docs was: {}".format(host[1]["Available RAM"])]
    })
    target_data = pd.concat([target_data, new_data])

target_data.to_csv(target_servers_file, index=False)