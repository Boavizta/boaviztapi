#!/usr/bin/python3

import pandas as pd
from pprint import pprint
import re
from math import ceil

target_data = pd.DataFrame({
    "id": [],
    "manufacturer": [],
    "CASE.case_type": [],
    "CPU.units": [],
    "CPU.core_units": [],
    "CPU.die_size_per_core": [],
    #"CPU.tdp": [],
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
source_instances_host_mapping = "instance_host.csv"
source_manual_instances_host_mapping = "manual_instance_host_cleaned.csv"
source_vantage_instances_file = "azure_vms_from_vantage.csv"
target_instances_file = "azure_instances.csv"

data = pd.read_csv(source_dedicated_hosts_file)
manual_instances_host_mapping = pd.read_csv(source_manual_instances_host_mapping)
instances_host_mapping = pd.read_csv(source_instances_host_mapping, header=None)
vantage_data = pd.read_csv(source_vantage_instances_file)

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

def get_instances_per_host(instances_host_mapping, host_name):
    manual_data = manual_instances_host_mapping.copy()
    manual_data.columns = range(manual_data.shape[1])
    instances_host_mapping = pd.concat([
        instances_host_mapping, manual_data[[0, 1]]
    ])
    # TODO: mapping instance -> hostS, when multiple instance refs with different hosts
    # build a min;avg;max mapping, put it in host cell for this instance in the resulting dataframe
    # gen both result.csv in the old fashion way and new result.csv with the new mapping, compare differences in per-instance impact
    mapping = instances_host_mapping[instances_host_mapping[1] == host_name.lower()][0]
    instances_data = pd.DataFrame({
        "id": [],
        "vcpu": [],
        "memory": [],
        "ssd_storage": [],
        "hdd_storage": [],
        "gpu_units": [],
        "platform": [],
        "source": []
    })
    for instance in mapping:
        instance = instance.replace(" ", "_")
        from_vantage = vantage_data[vantage_data["Name"].str.lower() == instance.replace("_", " ")]
        from_vantage_by_api_name = vantage_data[vantage_data["API Name"].str.lower() == instance.replace("_", " ")]

        vcpus = from_vantage["vCPUs"].str.replace(" vCPUs", "")
        if len(vcpus.index) == 0:
            vcpus = from_vantage_by_api_name["vCPUs"].str.replace(" vCPUs", "")
        mem = from_vantage["Instance Memory"].str.replace(" GiB", "")
        if len(mem.index) == 0:
            mem = from_vantage_by_api_name["Instance Memory"].str.replace(" GiB", "")
        gpus = from_vantage["GPUs"].str.replace(r"", "", regex=True)
        if len(gpus.index) == 0:
            gpus = from_vantage_by_api_name["GPUs"].str.replace(r"", "", regex=True)
        ssd_sto = from_vantage["Instance Storage"]
        if len(ssd_sto.index) == 0:
            ssd_sto = from_vantage_by_api_name["Instance Storage"]
        if len(ssd_sto.index) > 0:
            ssd_sto_value = ssd_sto.values[0]
        else:
            ssd_sto_value = 0
        # if we also have NVMe local ssd storage for the instance, add it to ssd_sto
        data_from_manual_mapping = manual_instances_host_mapping[manual_instances_host_mapping["instance"] == instance.replace("standard_", "")]
        if len(data_from_manual_mapping.index) > 0:
            if data_from_manual_mapping["nvme_units"].values[0] != "NaN" and data_from_manual_mapping["nvme_units"].values[0] > 0:
                if data_from_manual_mapping["nvme_capacity"].values[0] != "NaN" and data_from_manual_mapping["nvme_capacity"].values[0] > 0:
                    ssd_sto_value = float(ssd_sto_value) + float(data_from_manual_mapping["nvme_units"].values[0]) * float(data_from_manual_mapping["nvme_capacity"].values[0])
        else:
            print("Couldn't find {} in manual_instance_mapping".format(instance.replace("standard_", "")))
        # if we have so bad data that we don't know at least for vcpus and memory, discard the instance
        if len(vcpus.index) > 0 or len(mem.index) > 0:
            instances_data = pd.concat(
                [
                    instances_data,
                    pd.DataFrame({
                        "id": [instance],
                        "vcpu": [vcpus.values[0] if len(vcpus.index) > 0 else 0],
                        "memory": [mem.values[0] if len(mem.index) > 0 else 0],
                        "ssd_storage": [ssd_sto_value],
                        # TODO: change default SSD value for average of all default storage
                        "hdd_storage": [0],
                        "gpu_units": [gpus.values[0] if len(gpus.index) > 0 else 0],
                        # TODO fetch GPU units per instance
                        "platform": [host_name],
                        "source": ["Vantage for instance specs (https://instances.vantage.sh/azure/), Azure docs for instance-host mapping, see README for details."]
                    })
                ]
            )
    return instances_data

def get_instance_gpus_from_vantage(instance_name):
    res = vantage_data.loc[vantage_data["Name"].str.lower() == instance_name]
    return res

def get_disks_per_platform(platform_data, instances_per_host):
    res = {
        "ssd": {
            "units": 0,
            "capacity": 0
        },
        "hdd": {
            "units": 0,
            "capacity": 0
        }
    }
    ssd_sto_platform = 0
    hdd_sto_platform = 0
    # if we have the max number of instance per host in the manual mapping data
    manual_data = manual_instances_host_mapping[manual_instances_host_mapping["host"] == platform_data["id"].lower()]
    if len(manual_data.index) > 0:
        for i in manual_data[["instance", "host", "nbinstancesmax"]].iterrows():
            if float(i[1]["nbinstancesmax"]) > 0.0:
                instance_data = instances_per_host[instances_per_host["id"] == i[1]["instance"]]
                if len(instance_data["ssd_storage"].index) > 0 and instance_data["ssd_storage"].values[0] * i[1]["nbinstancesmax"] > ssd_sto_platform:
                    ssd_sto_platform = float(instance_data["ssd_storage"].values[0]) * float(i[1]["nbinstancesmax"])
    else: 
    #  else get instance with highest vcpus count
        max_vcpu_instances = instances_per_host[instances_per_host["vcpu"]==instances_per_host["vcpu"].max()]
        if len(max_vcpu_instances.index) > 0:
            max_vcpus_per_instance = max_vcpu_instances["vcpu"].values[0]
            # divide the maximum vcpus count of the host by this max instance vcpus
            max_vcpus_on_host = int(platform_data["vcpus"])
            ratio = max_vcpus_on_host / float(max_vcpus_per_instance)
            # to get how many vms of this type can run on the host : nb_{i}_on_{h}
            # get ssd and hdd units and capacity for this instance
            # multiply those values by nb_{i}_on_{h}, apply to res, return
            ssd_sto_platform = ratio * max_vcpu_instances["ssd_storage"].values[0]
            hdd_sto_platform = ratio * max_vcpu_instances["hdd_storage"].values[0]
            # As we don't have better information so far regarding underlying storage infrastructure, we use an
            # empirical hypothesis that SSD drives are most probably bigger than 2TB and HDD drives bigger than 4TB
    # whatever the source of information we consider at least 2TB capacity per drive
    res["ssd"]["units"] = ceil(ssd_sto_platform / 2048.0)
    if res["ssd"]["units"] > 0:
        res["ssd"]["capacity"] = 2048
    else:
        res["ssd"]["capacity"] = 0
    res["hdd"]["units"] = ceil(hdd_sto_platform / 4096.0)
    if res["hdd"]["units"] > 0:
        res["hdd"]["capacity"] = 4096
    else:
        res["hdd"]["capacity"] = 0
    return res

cpu_specs = pd.read_csv(source_cpu_spec_file)
hosts_matching_no_instance = []
instance_host_mapping = pd.DataFrame(
    {
        "id": [],
        "vcpu": [],
        "memory": [],
        "ssd_storage": [],
        "hdd_storage": [],
        "gpu_units": [],
        "platform": [],
        "source": []
    }
)

for host in data[["Dedicated Host SKUs (VM series and Host Type)", "Available vCPUs","Available RAM","CPU"]].iterrows():
    #
    # Get CPU specification for the current host
    #
    current_cpu_spec = get_cpu_spec(cpu_specs, host[1]["CPU"])
    current_host_name = host[1]["Dedicated Host SKUs (VM series and Host Type)"]
    if current_cpu_spec is None:
        print("No spec found for: {}".format(host[1]["CPU"]))
    else:
        print("CPU: {} threads: {} host max vCPU : {} supposed CPU units: {}".format(current_cpu_spec["name"], current_cpu_spec["threads"], host[1]["Available vCPUs"], get_cpu_units(host[1], current_cpu_spec)))
    current_gpu = get_gpu_from_string(host[1]["CPU"])
    instances_per_host = get_instances_per_host(instances_host_mapping, current_host_name)
    if instances_per_host is None or len(instances_per_host.index) == 0:
        print("host {} not macthing any instance !!!".format(current_host_name))
        hosts_matching_no_instance.append(current_host_name)
    else:
        #
        # Make a mapping instance to host
        #
        instance_host_mapping = pd.concat([instance_host_mapping, instances_per_host])
    #
    # If there are GPUs on this host
    # Get how many GPUs are allocated to virtual machines deployed on current host, as a maximum
    # TODO FIX
    #
    #if current_gpu is not None:
    #    print("Current GPU: {}".format(current_gpu))
    #    for i in instances_per_host:
    #        instance_gpus = get_instance_gpus_from_vantage(i["instance_name"])
    #        if len(instance_gpus.index) > 0:
    #            print("Instance: {} GPU: {}".format(i["instance_name"], instance_gpus))
    #        else:
    #            print("Host {} has GPUs ({}) but instance {} has not".format(current_host_name, current_gpu, i["instance_name"]))

    nb_of_sticks, stick_capacity = compute_ram_sticks(host[1]["Available RAM"])
    platform_id = host[1]["Dedicated Host SKUs (VM series and Host Type)"]
    cpu_units = get_cpu_units(host[1], current_cpu_spec)
    disks_hypothesis = get_disks_per_platform(
        {"id": platform_id, "vcpus": host[1]["Available vCPUs"]},
        instances_per_host
    )
    new_data = pd.DataFrame({
        "id": [platform_id],
        "manufacturer": ["Azure"],
        "CASE.case_type": ["rack"], # TODO: source from Azure docs which platform is blade, which is rack
        "CPU.units": [cpu_units],
        "CPU.core_units": [""],
        "CPU.die_size_per_core": [""],
        #"CPU.tdp": [current_cpu_spec["tdp"] if current_cpu_spec is not None else ""],
        "CPU.name": [current_cpu_spec["name"] if current_cpu_spec is not None else ""],
        "CPU.vcpu": [host[1]["Available vCPUs"]],
        "RAM.units": [nb_of_sticks],
        "RAM.capacity": [stick_capacity],
        "SSD.units": [disks_hypothesis["ssd"]["units"]], # TODO: get hypothesis that seem close to what users see on those machines
        "SSD.capacity": [disks_hypothesis["ssd"]["capacity"]],
        "HDD.units": [disks_hypothesis["hdd"]["units"]],
        "HDD.capacity": [disks_hypothesis["hdd"]["capacity"]],
        "GPU.units": [0], # TODO: guess it from how many GPUs have the biggest instances hosted on this platform
        "GPU.name": [current_gpu],
        "GPU.memory_capacity": [""],
        "POWER_SUPPLY.units": ["2;2;2"], # TODO: source from Azure docs which platform is blade, which is rack
        "POWER_SUPPLY.unit_weight": ["2.99;1;5"], # TODO: source from Azure docs which platform is blade, which is rack
        "USAGE.time_workload": ["50;0;100"],
        "USAGE.use_time_ratio": ["1"],
        "USAGE.hours_life_time": [52560], # According to latest news, Azure extended servers lifetime from 4 to 6 years. (https://www.networkworld.com/article/971373/microsoft-extends-azure-server-lifetimes-by-50.html)
        "USAGE.other_consumption_ratio": ["0.33;0.2;0.6"], # TODO: challenge those factors based on azure actual hardware
        "WARNINGS": ["RAM units and per unit capacity not verified. RAM capacity from Azure docs was: {}".format(host[1]["Available RAM"])]
    })
    target_data = pd.concat([target_data, new_data])

print("Hosts matching no instance: ")
pprint(hosts_matching_no_instance)
instance_host_mapping.to_csv(target_instances_file, index=False)

target_data.to_csv(target_servers_file, index=False)
