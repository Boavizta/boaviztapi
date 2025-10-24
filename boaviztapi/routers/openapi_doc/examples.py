def convert_to_openapi_example(configuration_examples):
    return {k: {"summary": "{example}".format(example=k), "value": v} for k, v in configuration_examples.items()}


server_configuration_examples = {
    "emptyserver": {},
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

server_configuration_examples_openapi = convert_to_openapi_example(server_configuration_examples)

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
            "usage": {
                "usage_location": "FRA"
            }
        }
    },
    "ssd": {
        "custom ssd": {
            "capacity": 500,
            "manufacturer": "Samsung",
        },
        "empty ssd": {}
    },
    "ram": {
        "custom ram": {
            "capacity": 32,
            "manufacturer": "Samsung",
            "process": 30.0
        },
        "empty ram": {}
    },
    "hdd": {
        "empty HDD": {}
    },
    "motherboard": {
        "empty motherboard": {}
    },
    "power_supply": {
        "custom power supply": {
            "unit_weight": 10
        }
    },
    "case": {
        "rack": {
            "case_type": "rack"
        },
        "blade": {
            "case_type": "blade"
        }
    }
}

components_examples_openapi = {
    "cpu": convert_to_openapi_example(components_examples["cpu"]),
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
        }, {
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

electricity_power_breakdown = {
    "zone": "AT",
    "datetime": "2025-10-17T11:00:00.000Z",
    "updatedAt": "2025-10-17T10:39:53.914Z",
    "createdAt": "2025-10-14T23:26:15.840Z",
    "powerConsumptionBreakdown": {
        "nuclear": 275,
        "geothermal": 0,
        "biomass": 426,
        "coal": 734,
        "wind": 422,
        "solar": 1611,
        "hydro": 1976,
        "gas": 1484,
        "oil": 10,
        "unknown": 26,
        "hydro discharge": 420,
        "battery discharge": 0
    },
    "powerProductionBreakdown": {
        "nuclear": None,
        "geothermal": 0,
        "biomass": 358,
        "coal": 0,
        "wind": 132,
        "solar": 1292,
        "hydro": 2226,
        "gas": 1438,
        "oil": 0,
        "unknown": 22,
        "hydro discharge": 438,
        "battery discharge": None
    },
    "powerImportBreakdown": {
        "CH": 0,
        "CZ": 910,
        "DE": 1824,
        "HU": 0,
        "SI": 0,
        "IT-NO": 0
    },
    "powerExportBreakdown": {
        "CH": 67,
        "CZ": 0,
        "DE": 0,
        "HU": 53,
        "SI": 934,
        "IT-NO": 200
    },
    "fossilFreePercentage": 69,
    "renewablePercentage": 66,
    "powerConsumptionTotal": 7385,
    "powerProductionTotal": 5905,
    "powerImportTotal": 2734,
    "powerExportTotal": 1254,
    "isEstimated": True,
    "estimationMethod": "TIME_SLICER_AVERAGE",
    "temporalGranularity": "hourly"
}

electricity_carbon_intensity = {
    "zone": "AT",
    "carbonIntensity": 245,
    "datetime": "2025-10-17T11:00:00.000Z",
    "updatedAt": "2025-10-17T10:39:53.914Z",
    "createdAt": "2025-10-14T23:26:15.840Z",
    "emissionFactorType": "lifecycle",
    "isEstimated": True,
    "estimationMethod": "TIME_SLICER_AVERAGE",
    "temporalGranularity": "hourly"
}

electricity_maps_price = {
    "zone": "AT",
    "datetime": "2025-10-24T10:00:00.000Z",
    "createdAt": "2025-10-23T11:21:05.983Z",
    "updatedAt": "2025-10-23T11:21:05.983Z",
    "value": 82.4,
    "unit": "EUR/MWh",
    "source": "nordpool.com",
    "temporalGranularity": "hourly"
}
