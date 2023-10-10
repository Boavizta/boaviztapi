server_configuration_examples = {
    "DellR740": {"model":
            {
                "type": "rack"

            },
        "configuration":
            {
                "cpu":
                    {
                        "units": 2,
                        "name": "intel xeon gold 6134"
                    },
                "ram":
                    [
                        {
                            "units": 12,
                            "capacity": 32

                        }
                    ],
                "disk":
                    [
                        {
                            "units": 1,
                            "type": "ssd",
                            "capacity": 400,
                            "density": 50.6
                        }
                    ]
            },
        "usage": {
            "avg_power": 300,
            "usage_location": "FRA"
        }
    }}

components_examples = {
    "cpu": {
        "name": "intel xeon gold 6134",
    },
    "ssd": {
        "capacity": 24,
        "manufacturer": "Samsung",
    },
    "ram": {
        "capacity": 32,
        "manufacturer": "Samsung",
        "process": 30.0
    },
    "hdd": {},
    "motherboard": {},
    "power_supply": {
        "unit_weight": 10
    },
    "case": {"case_type": "rack"},
}

cloud_usage_example = {
        "usage_location": "FRA",
        "time_workload": [
            {"time_percentage": 50, "load_percentage": 0},
            {"time_percentage": 25, "load_percentage": 60},
            {"time_percentage": 25, "load_percentage": 100}
        ]
}

cloud_example = {
    "provider": "aws",
    "instance_type": "a1.4xlarge",
    "usage":
            {
            "usage_location": "FRA",
            "time_workload": [
                {"time_percentage": 50, "load_percentage": 0},
                {"time_percentage": 25, "load_percentage": 60},
                {"time_percentage": 25, "load_percentage": 100}
            ]}
}

cpu_consumption_profiles = {
        "cpu": {
            "name": "intel xeon gold 6134"
        },
        "workload": [
            {
                "load_percentage": 0,
                "power_watt": 50
            },
            {
                "load_percentage": 10,
                "power_watt": 100
            },{
                "load_percentage": 50,
                "power_watt": 180
            },
            {
                "load_percentage": 100,
                "power_watt": 245
            }
        ],
}

end_user_terminal = {
    "usage": {
        "use_time_ratio": 0.3,
        "usage_location": "FRA",
    }
}