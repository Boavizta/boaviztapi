server_configuration_examples = {
    "DellR740": {
        "model":
            {
                "manufacturer": "Dell",
                "name": "R740",
                "type": "rack",
                "year": 2020,
                "archetype": "dellR740"
            },
        "configuration":
            {
                "cpu":
                    {
                        "units": 2,
                        "core_units": 24,
                        "die_size_per_core": 0.245
                    },
                "ram":
                    [
                        {
                            "units": 12,
                            "capacity": 32,
                            "density": 1.79
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
                    ],
                "power_supply":
                    {
                        "units": 2,
                        "unit_weight": 2.99
                    }
            },
        "usage": {
            "max_power": 510,
            "years_use_time": 1,
            "days_use_time": 1,
            "hours_use_time": 1,
            "workload": {
                "100": {
                    "time": 0.15,
                    "power": 1.0
                },
                "50": {
                    "time": 0.55,
                    "power": 0.7235
                },
                "10": {
                    "time": 0.2,
                    "power": 0.5118
                },
                "idle": {
                    "time": 0.1,
                    "power": 0.3941
                }
            }
        }
    },
}
components_examples = {
    "cpu": {
        "core_units": 24,
        "family": "Skylake",
        "manufacture_date": 2017
    },
    "ssd": {
        "core_units": 24,
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
    "1": {
        "hours_use_time": 2,
        "usage_location": "FRA",
        "workload": {
            '10': {
                'time': 0
            },
            '50': {
                'time': 1
            },
            '100': {
                'time': 0
            },
            'idle': {
                'time': 0
            }
        }
    }
}
