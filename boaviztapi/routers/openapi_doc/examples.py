def convert_to_openapi_example(configuration_examples):
    return {
        k: {"summary": "{example}".format(example=k), "value": v}
        for k, v in configuration_examples.items()
    }


server_configuration_examples = {
    "emptyserver": {},
    "DellR740": {
        "model": {"type": "rack"},
        "configuration": {
            "cpu": {"units": 2, "name": "intel xeon gold 6134"},
            "ram": [{"units": 12, "capacity": 32}],
            "disk": [{"units": 1, "type": "ssd", "capacity": 400, "density": 50.6}],
        },
        "usage": {"avg_power": 300, "usage_location": "FRA"},
    },
}

server_configuration_examples_openapi = convert_to_openapi_example(
    server_configuration_examples
)

components_examples = {
    "cpu": {
        "intel xeon gold 6134": {
            "name": "intel xeon gold 6134",
        },
        "empty cpu": {},
        "custom cpu": {
            "core_units": 64,
            "tdp": 150,
            "die_size": 400,
            "usage": {"usage_location": "FRA"},
        },
    },
    "gpu": {
        "custom gpu": {
            "weight": 1.69,
            "heatsink_weight": 0.90077,
            "pwb_surface": 296.37,
            "casing_weight": 0.78923,
            "gpu_surface": 2810.4,
            "vram": 80,
            "vram_dies": 6,
            "transport_boat": 19000,
            "transport_truck": 1000,
            "transport_plane": 0,
            "usage": {"usage_location": "FRA"},
        },
    },
    "ssd": {
        "custom ssd": {
            "capacity": 500,
            "manufacturer": "Samsung",
        },
        "empty ssd": {},
    },
    "ram": {
        "custom ram": {"capacity": 32, "manufacturer": "Samsung", "process": 30.0},
        "empty ram": {},
    },
    "hdd": {"empty HDD": {}},
    "motherboard": {"empty motherboard": {}},
    "power_supply": {"custom power supply": {"unit_weight": 10}},
    "case": {"rack": {"case_type": "rack"}, "blade": {"case_type": "blade"}},
}

components_examples_openapi = {
    "cpu": convert_to_openapi_example(components_examples["cpu"]),
    "gpu": convert_to_openapi_example(components_examples["gpu"]),
    "ram": convert_to_openapi_example(components_examples["ram"]),
    "ssd": convert_to_openapi_example(components_examples["ssd"]),
    "hdd": convert_to_openapi_example(components_examples["hdd"]),
    "motherboard": convert_to_openapi_example(components_examples["motherboard"]),
    "power_supply": convert_to_openapi_example(components_examples["power_supply"]),
    "case": convert_to_openapi_example(components_examples["case"]),
}

cloud_usage_example = {
    "usage_location": "FRA",
    "time_workload": [
        {"time_percentage": 50, "load_percentage": 0},
        {"time_percentage": 25, "load_percentage": 60},
        {"time_percentage": 25, "load_percentage": 100},
    ],
}

cloud_example = {
    "provider": "aws",
    "instance_type": "a1.4xlarge",
    "usage": {
        "usage_location": "FRA",
        "time_workload": [
            {"time_percentage": 50, "load_percentage": 0},
            {"time_percentage": 25, "load_percentage": 60},
            {"time_percentage": 25, "load_percentage": 100},
        ],
    },
}

cpu_consumption_profiles = {
    "cpu": {"name": "intel xeon gold 6134"},
    "workload": [
        {"load_percentage": 0, "power_watt": 50},
        {"load_percentage": 10, "power_watt": 100},
        {"load_percentage": 50, "power_watt": 180},
        {"load_percentage": 100, "power_watt": 245},
    ],
}

end_user_terminal = {
    "usage": {
        "use_time_ratio": 0.3,
        "usage_location": "FRA",
    }
}
