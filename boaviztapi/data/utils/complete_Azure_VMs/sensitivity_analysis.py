from requests import post
from json import dumps
from csv import DictWriter

BOAVIZTAPI_CONTAINER_URL = "http://0.0.0.0:5000/v1/server/"
RESULT_FILE = "sensitivity_analysis_hosts_with_ssd.csv"

query = {"verbose": "false", "criteria": "gwp"}

dasv4_type2 = {
    "model": {"type": "rack"},
    "configuration": {
        "cpu": {"units": 1, "name": "amd epyc 7763"},
        "ram": [{"units": 48, "capacity": 16}],
        "disk": [
            {
                "units": 0,
                "type": "ssd",
                "capacity": 0,
                "density": 50.6,
            }
        ],
    },
    "usage": {"avg_power": 300, "usage_location": "FRA"},
}

dcsv2_type1 = {
    "model": {"type": "rack"},
    "configuration": {
        "cpu": {"units": 1, "name": "intel xeon e-2288g"},
        "ram": [{"units": 8, "capacity": 8}],
        "disk": [
            {
                "units": 0,
                "type": "ssd",
                "capacity": 0,
                "density": 50.6,
            }
        ],
    },
    "usage": {"avg_power": 300, "usage_location": "FRA"},
}

msv2_type1 = {
    "model": {"type": "rack"},
    "configuration": {
        "cpu": {"units": 8, "name": "intel xeon platinum 8180m"},
        "ram": [{"units": 48, "capacity": 64}],
        "disk": [
            {
                "units": 0,
                "type": "ssd",
                "capacity": 0,
                "density": 50.6,
            }
        ],
    },
    "usage": {"avg_power": 300, "usage_location": "FRA"},
}

hosts = {
    "dcsv2_type1": dcsv2_type1,
    "dasv4_type2": dasv4_type2,
    "msv2_type1": msv2_type1,
}


def get_manufacturing_impact_with_ssd(host, ssd_units, ssd_capacity):

    host["configuration"]["disk"][0]["units"] = ssd_units
    host["configuration"]["disk"][0]["capacity"] = ssd_capacity

    request = post(BOAVIZTAPI_CONTAINER_URL, params=query, data=dumps(host))
    server_data = request.json()
    lifetime_manufacturing_impact = server_data["impacts"]["gwp"]["embedded"]["value"]
    return lifetime_manufacturing_impact


with open(RESULT_FILE, newline="", mode="w") as result_file:
    fieldnames = [
        "id",
        "cpu",
        "impact_manufacturing_no_ssd",
        "impact_manufacturing_ssd_1024_gib",
        "impact_manufacturing_ssd_2048_gib",
        "impact_manufacturing_ssd_4096_gib",
        "impact_manufacturing_ssd_8192_gib",
        "impact_manufacturing_ssd_16384_gib",
    ]
    result_writer = DictWriter(result_file, fieldnames)
    result_writer.writeheader()
    for host in hosts:
        result_writer.writerow(
            {
                "id": host,
                "cpu": hosts[host]["configuration"]["cpu"]["name"],
                "impact_manufacturing_no_ssd": get_manufacturing_impact_with_ssd(
                    hosts[host], 0, 0
                ),
                "impact_manufacturing_ssd_1024_gib": get_manufacturing_impact_with_ssd(
                    hosts[host], 1, 1024
                ),
                "impact_manufacturing_ssd_2048_gib": get_manufacturing_impact_with_ssd(
                    hosts[host], 1, 2048
                ),
                "impact_manufacturing_ssd_4096_gib": get_manufacturing_impact_with_ssd(
                    hosts[host], 1, 4096
                ),
                "impact_manufacturing_ssd_8192_gib": get_manufacturing_impact_with_ssd(
                    hosts[host], 1, 8192
                ),
                "impact_manufacturing_ssd_16384_gib": get_manufacturing_impact_with_ssd(
                    hosts[host], 1, 16384
                ),
            }
        )
