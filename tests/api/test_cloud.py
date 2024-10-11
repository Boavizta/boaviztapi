import pytest
from httpx import AsyncClient

from boaviztapi.main import app

from dataclasses import dataclass
from .util import (
    CloudInstanceRequest,
    ADPImpact,
    GWPImpact,
    PEImpact,
    ImpactOutput,
    END_OF_LIFE_WARNING,
    UNCERTAINTY_WARNING,
)

pytest_plugins = ("pytest_asyncio",)


@dataclass
class CloudTest:
    request: CloudInstanceRequest

    adp: ADPImpact
    gwp: GWPImpact
    pe: PEImpact

    verbose_output: str = None

    async def check_result(self):
        url = self.request.to_url()
        body = self.request.to_dict()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            if self.request.use_url_params:
                res = await ac.get(url)
            else:
                res = await ac.post(url, json=body)

        expected = {
            "impacts": {
                "adp": self.adp.to_dict(),
                "gwp": self.gwp.to_dict(),
                "pe": self.pe.to_dict(),
            },
        }

        assert res.json() == expected


@pytest.mark.asyncio
async def test_empty_usage():
    test = CloudTest(
        CloudInstanceRequest("aws", "a1.4xlarge"),
        ADPImpact(
            ImpactOutput(0.1414, 0.06512, 0.099, END_OF_LIFE_WARNING),
            ImpactOutput(0.000581, 2.165e-05, 0.00012),
        ),
        GWPImpact(
            ImpactOutput(635.6, 258.0, 450.0, END_OF_LIFE_WARNING),
            ImpactOutput(1969.0, 37.73, 700.0),
        ),
        PEImpact(
            ImpactOutput(8833.0, 3529.0, 6300.0, END_OF_LIFE_WARNING),
            ImpactOutput(1024000.0, 21.33, 20000.0, UNCERTAINTY_WARNING),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_empty_usage_m6gxlarge():
    test = CloudTest(
        CloudInstanceRequest("aws", "m6g.xlarge"),
        ADPImpact(
            ImpactOutput(0.01088, 0.005075, 0.0075, END_OF_LIFE_WARNING),
            ImpactOutput(0.0001721, 6.415e-06, 3e-05),
        ),
        GWPImpact(
            ImpactOutput(89.17, 31.52, 55.0, END_OF_LIFE_WARNING),
            ImpactOutput(583.2, 11.18, 200.0),
        ),
        PEImpact(
            ImpactOutput(1167.0, 415.6, 730.0, END_OF_LIFE_WARNING),
            ImpactOutput(303400.0, 6.318, 10000.0),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_empty_usage_with_url_params_a1():
    test = CloudTest(
        CloudInstanceRequest("aws", "a1.2xlarge", use_url_params=True),
        ADPImpact(
            ImpactOutput(0.07069, 0.03256, 0.049, END_OF_LIFE_WARNING),
            ImpactOutput(0.0002905, 1.083e-05, 6e-05),
        ),
        GWPImpact(
            ImpactOutput(317.8, 129.0, 230.0, END_OF_LIFE_WARNING),
            ImpactOutput(984.3, 18.87, 350.0),
        ),
        PEImpact(
            ImpactOutput(4416.0, 1764.0, 3200.0, END_OF_LIFE_WARNING),
            ImpactOutput(512000.0, 10.66, 10000.0),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_empty_usage_with_url_params_r5ad():
    test = CloudTest(
        CloudInstanceRequest("aws", "r5ad.12xlarge", use_url_params=True),
        ADPImpact(
            ImpactOutput(0.1206, 0.06419, 0.086, END_OF_LIFE_WARNING),
            ImpactOutput(0.003295, 0.0001228, 0.0007),
        ),
        GWPImpact(
            ImpactOutput(1693.0, 592.6, 1000.0, END_OF_LIFE_WARNING),
            ImpactOutput(11170.0, 214.0, 4000.0),
        ),
        PEImpact(
            ImpactOutput(21470.0, 7590.0, 13000.0, END_OF_LIFE_WARNING),
            ImpactOutput(5808000.0, 121.0, 100000.0),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_wrong_input():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false",
            json={"provider": "test", "instance_type": "a1.4xlarge", "usage": {}},
        )
    assert res.json() == {"detail": "a1.4xlarge at test not found"}


@pytest.mark.asyncio
async def test_wrong_input_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false",
            json={"provider": "aws", "instance_type": "test", "usage": {}},
        )
    assert res.json() == {"detail": "test at aws not found"}


@pytest.mark.asyncio
async def test_usage_with_complex_time_workload():
    test = CloudTest(
        CloudInstanceRequest(
            "aws",
            "c5a.24xlarge",
            usage={
                "time_workload": [
                    {"time_percentage": 50, "load_percentage": 0},
                    {"time_percentage": 25, "load_percentage": 60},
                    {"time_percentage": 25, "load_percentage": 100},
                ]
            },
        ),
        ADPImpact(
            ImpactOutput(0.1744, 0.08626, 0.124, END_OF_LIFE_WARNING),
            ImpactOutput(0.002975, 0.0001109, 0.0006),
        ),
        GWPImpact(
            ImpactOutput(1215.0, 458.4, 780.0, END_OF_LIFE_WARNING),
            ImpactOutput(10080.0, 193.2, 3500.0),
        ),
        PEImpact(
            ImpactOutput(16070.0, 6108.0, 10500.0, END_OF_LIFE_WARNING),
            ImpactOutput(5244000.0, 109.2, 100000.0),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_usage_with_simple_time_workload():
    test = CloudTest(
        CloudInstanceRequest(
            "aws",
            "c5a.24xlarge",
            usage={"time_workload": 100},
        ),
        ADPImpact(
            ImpactOutput(0.1744, 0.08626, 0.124, END_OF_LIFE_WARNING),
            ImpactOutput(0.005068, 0.0001889, 0.001),
        ),
        GWPImpact(
            ImpactOutput(1215.0, 458.4, 780.0, END_OF_LIFE_WARNING),
            ImpactOutput(17170.0, 329.2, 6000.0),
        ),
        PEImpact(
            ImpactOutput(16070.0, 6108.0, 10500.0, END_OF_LIFE_WARNING),
            ImpactOutput(8934000.0, 186.1, 200000.0),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_usage_with_duration():
    test = CloudTest(
        CloudInstanceRequest(
            "aws",
            "c5a.24xlarge",
            duration=1,
        ),
        ADPImpact(
            ImpactOutput(4.977e-06, 2.462e-06, 3.5e-06, END_OF_LIFE_WARNING),
            ImpactOutput(1.122e-07, 4.182e-09, 2e-08),
        ),
        GWPImpact(
            ImpactOutput(0.03467, 0.01308, 0.022, END_OF_LIFE_WARNING),
            ImpactOutput(0.3802, 0.007287, 0.13),
        ),
        PEImpact(
            ImpactOutput(0.4588, 0.1743, 0.3, END_OF_LIFE_WARNING),
            ImpactOutput(197.8, 0.004119, 5.0, UNCERTAINTY_WARNING),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_usage_with_duration_and_time_workload():
    test = CloudTest(
        CloudInstanceRequest(
            "aws",
            "a1.4xlarge",
            duration=2,
            usage={
                "usage_location": "FRA",
                "time_workload": [
                    {"time_percentage": "50", "load_percentage": "0"},
                    {"time_percentage": "50", "load_percentage": "50"},
                ],
            },
        ),
        ADPImpact(
            ImpactOutput(8.07e-06, 3.717e-06, 5.6e-06, END_OF_LIFE_WARNING),
            ImpactOutput(4.11e-09, 3.082e-09, 3.4e-09),
        ),
        GWPImpact(
            ImpactOutput(0.03628, 0.01472, 0.026, END_OF_LIFE_WARNING),
            ImpactOutput(0.008291, 0.006218, 0.0069),
        ),
        PEImpact(
            ImpactOutput(0.5041, 0.2014, 0.36, END_OF_LIFE_WARNING),
            ImpactOutput(0.955, 0.7163, 0.79),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_verbose_output_with_empty_usage():
    test = CloudTest(
        CloudInstanceRequest("aws", "r5ad.12xlarge", use_url_params=True),
        ADPImpact(
            ImpactOutput(0.1206, 0.06419, 0.086, END_OF_LIFE_WARNING),
            ImpactOutput(0.003295, 0.0001228, 0.0007),
        ),
        GWPImpact(
            ImpactOutput(1693.0, 592.6, 1000.0, END_OF_LIFE_WARNING),
            ImpactOutput(11170.0, 214.0, 4000.0),
        ),
        PEImpact(
            ImpactOutput(21470.0, 7590.0, 13000.0, END_OF_LIFE_WARNING),
            ImpactOutput(5808000.0, 121.0, 100000.0),
        ),
        verbose_output={
            "ASSEMBLY-1": {
                "duration": {"unit": "hours", "value": 35040.0},
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and fossil ressources",
                        "embedded": {
                            "max": 5.288e-07,
                            "min": 5.288e-07,
                            "value": 5.288e-07,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": "not implemented",
                    },
                    "gwp": {
                        "description": "Total climate change",
                        "embedded": {
                            "max": 2.505,
                            "min": 2.505,
                            "value": 2.505,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": "not implemented",
                    },
                    "pe": {
                        "description": "Consumption of primary energy",
                        "embedded": {
                            "max": 25.72,
                            "min": 25.72,
                            "value": 25.72,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": "not implemented",
                    },
                },
                "units": {"max": 1, "min": 1, "status": "ARCHETYPE", "value": 1},
            },
            "CASE-1": {
                "case_type": {"status": "ARCHETYPE", "value": "rack"},
                "duration": {"unit": "hours", "value": 35040.0},
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and fossil ressources",
                        "embedded": {
                            "max": 0.01038,
                            "min": 0.007575,
                            "value": 0.0076,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": "not implemented",
                    },
                    "gwp": {
                        "description": "Total climate change",
                        "embedded": {
                            "max": 56.25,
                            "min": 32.21,
                            "value": 56.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": "not implemented",
                    },
                    "pe": {
                        "description": "Consumption of primary energy",
                        "embedded": {
                            "max": 825.0,
                            "min": 460.8,
                            "value": 820.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": "not implemented",
                    },
                },
                "units": {"max": 1, "min": 1, "status": "ARCHETYPE", "value": 1},
            },
            "CPU-1": {
                "adp_factor": {
                    "max": 2.656e-07,
                    "min": 1.32e-08,
                    "source": "ADEME Base IMPACTS ®",
                    "status": "DEFAULT",
                    "unit": "kg Sbeq/kWh",
                    "value": 6.42e-08,
                },
                "avg_power": {
                    "max": 112.22999999999999,
                    "min": 112.22999999999999,
                    "status": "COMPLETED",
                    "unit": "W",
                    "value": 112.22999999999999,
                },
                "core_units": {
                    "max": 32,
                    "min": 32,
                    "source": "Completed from name name based on "
                    "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                    "status": "COMPLETED",
                    "value": 32,
                },
                "die_size": {
                    "max": 213.0,
                    "min": 213.0,
                    "source": "Average value of Naples with 32 cores",
                    "status": "COMPLETED",
                    "unit": "mm2",
                    "value": 213.0,
                },
                "duration": {"unit": "hours", "value": 35040.0},
                "family": {
                    "max": "Naples",
                    "min": "Naples",
                    "source": "Completed from name name based on "
                    "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                    "status": "COMPLETED",
                    "value": "Naples",
                },
                "gwp_factor": {
                    "max": 0.9,
                    "min": 0.023,
                    "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n"
                    "Average of 27 european countries",
                    "status": "DEFAULT",
                    "unit": "kg CO2eq/kWh",
                    "value": 0.38,
                },
                "hours_life_time": {
                    "max": 35040.0,
                    "min": 35040.0,
                    "source": "from device",
                    "status": "COMPLETED",
                    "unit": "hours",
                    "value": 35040.0,
                },
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and fossil ressources",
                        "embedded": {
                            "max": 0.0153,
                            "min": 0.0153,
                            "value": 0.0153,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": {"max": 0.002089, "min": 0.0001038, "value": 0.0005},
                    },
                    "gwp": {
                        "description": "Total climate change",
                        "embedded": {
                            "max": 10.73,
                            "min": 10.73,
                            "value": 10.73,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": {"max": 7079.0, "min": 180.9, "value": 3000.0},
                    },
                    "pe": {
                        "description": "Consumption of primary energy",
                        "embedded": {
                            "max": 169.1,
                            "min": 169.1,
                            "value": 169.1,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": {"max": 3682000.0, "min": 102.2, "value": 100000.0},
                    },
                },
                "manufacturer": {
                    "max": "AMD",
                    "min": "AMD",
                    "source": "Completed from name name based on "
                    "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                    "status": "COMPLETED",
                    "value": "AMD",
                },
                "model_range": {
                    "max": "EPYC",
                    "min": "EPYC",
                    "source": "Completed from name name based on "
                    "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                    "status": "COMPLETED",
                    "value": "EPYC",
                },
                "name": {
                    "max": "AMD EPYC 7571",
                    "min": "AMD EPYC 7571",
                    "source": "fuzzy match",
                    "status": "COMPLETED",
                    "value": "AMD EPYC 7571",
                },
                "params": {
                    "source": "From TDP",
                    "status": "COMPLETED",
                    "value": {
                        "a": 101.6958680014875,
                        "b": 0.06466257889658457,
                        "c": 20.451103146337097,
                        "d": -4.569671341827919,
                    },
                },
                "pe_factor": {
                    "max": 468.15,
                    "min": 0.013,
                    "source": "ADPf / (1-%renewable_energy)",
                    "status": "DEFAULT",
                    "unit": "MJ/kWh",
                    "value": 12.874,
                },
                "tdp": {
                    "max": 200,
                    "min": 200,
                    "source": "Completed from name name based on "
                    "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                    "status": "COMPLETED",
                    "unit": "W",
                    "value": 200,
                },
                "threads": {
                    "max": 64,
                    "min": 64,
                    "source": "Completed from name name based on "
                    "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                    "status": "COMPLETED",
                    "value": 64,
                },
                "time_workload": {
                    "max": 100.0,
                    "min": 0.0,
                    "status": "ARCHETYPE",
                    "unit": "%",
                    "value": 50.0,
                },
                "units": {"max": 2.0, "min": 2.0, "status": "ARCHETYPE", "value": 2.0},
                "usage_location": {
                    "status": "DEFAULT",
                    "unit": "CodSP3 - NCS Country Codes " "- NATO",
                    "value": "EEE",
                },
                "use_time_ratio": {
                    "max": 1.0,
                    "min": 1.0,
                    "status": "ARCHETYPE",
                    "unit": "/1",
                    "value": 1.0,
                },
                "workloads": {
                    "status": "COMPLETED",
                    "unit": "workload_rate:W",
                    "value": [
                        {"load_percentage": 0, "power_watt": 24.0},
                        {"load_percentage": 10, "power_watt": 64.0},
                        {"load_percentage": 50, "power_watt": 150.0},
                        {"load_percentage": 100, "power_watt": 204.0},
                    ],
                },
            },
            "MOTHERBOARD-1": {
                "duration": {"unit": "hours", "value": 35040.0},
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and fossil ressources",
                        "embedded": {
                            "max": 0.001384,
                            "min": 0.001384,
                            "value": 0.001384,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": "not implemented",
                    },
                    "gwp": {
                        "description": "Total climate change",
                        "embedded": {
                            "max": 24.79,
                            "min": 24.79,
                            "value": 24.79,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": "not implemented",
                    },
                    "pe": {
                        "description": "Consumption of primary energy",
                        "embedded": {
                            "max": 313.5,
                            "min": 313.5,
                            "value": 313.5,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": "not implemented",
                    },
                },
                "units": {"max": 1, "min": 1, "status": "ARCHETYPE", "value": 1},
            },
            "POWER_SUPPLY-1": {
                "duration": {"unit": "hours", "value": 35040.0},
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and fossil ressources",
                        "embedded": {
                            "max": 0.03112,
                            "min": 0.006225,
                            "value": 0.019,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": "not implemented",
                    },
                    "gwp": {
                        "description": "Total climate change",
                        "embedded": {
                            "max": 91.13,
                            "min": 18.23,
                            "value": 54.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": "not implemented",
                    },
                    "pe": {
                        "description": "Consumption of primary energy",
                        "embedded": {
                            "max": 1320.0,
                            "min": 264.0,
                            "value": 800.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": "not implemented",
                    },
                },
                "unit_weight": {
                    "max": 5.0,
                    "min": 1.0,
                    "status": "ARCHETYPE",
                    "unit": "kg",
                    "value": 2.99,
                },
                "units": {"max": 2.0, "min": 2.0, "status": "ARCHETYPE", "value": 2.0},
            },
            "RAM-1": {
                "adp_factor": {
                    "max": 2.656e-07,
                    "min": 1.32e-08,
                    "source": "ADEME Base IMPACTS ®",
                    "status": "DEFAULT",
                    "unit": "kg Sbeq/kWh",
                    "value": 6.42e-08,
                },
                "avg_power": {
                    "max": 109.05599999999998,
                    "min": 109.05599999999998,
                    "status": "COMPLETED",
                    "unit": "W",
                    "value": 109.05599999999998,
                },
                "capacity": {
                    "max": 32.0,
                    "min": 32.0,
                    "status": "ARCHETYPE",
                    "unit": "GB",
                    "value": 32.0,
                },
                "density": {
                    "max": 2.375,
                    "min": 0.625,
                    "source": "Average of 11 rows",
                    "status": "COMPLETED",
                    "unit": "GB/cm2",
                    "value": 1.2443636363636363,
                },
                "duration": {"unit": "hours", "value": 35040.0},
                "gwp_factor": {
                    "max": 0.9,
                    "min": 0.023,
                    "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n"
                    "Average of 27 european countries",
                    "status": "DEFAULT",
                    "unit": "kg CO2eq/kWh",
                    "value": 0.38,
                },
                "hours_life_time": {
                    "max": 35040.0,
                    "min": 35040.0,
                    "source": "from device",
                    "status": "COMPLETED",
                    "unit": "hours",
                    "value": 35040.0,
                },
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and " "fossil ressources",
                        "embedded": {
                            "max": 0.05899,
                            "min": 0.03047,
                            "value": 0.04,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": {"max": 0.02436, "min": 0.001211, "value": 0.006},
                    },
                    "gwp": {
                        "description": "Total climate change",
                        "embedded": {
                            "max": 1414.0,
                            "min": 418.3,
                            "value": 740.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": {"max": 82540.0, "min": 2109.0, "value": 35000.0},
                    },
                    "pe": {
                        "description": "Consumption of primary energy",
                        "embedded": {
                            "max": 17660.0,
                            "min": 5302.0,
                            "value": 9000.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": {"max": 42930000.0, "min": 1192.0, "value": 1000000.0},
                    },
                },
                "params": {
                    "source": "(ram_electrical_factor_per_go : 0.284) * (ram_capacity: 32.0) ",
                    "status": "COMPLETED",
                    "value": {"a": 9.088},
                },
                "pe_factor": {
                    "max": 468.15,
                    "min": 0.013,
                    "source": "ADPf / (1-%renewable_energy)",
                    "status": "DEFAULT",
                    "unit": "MJ/kWh",
                    "value": 12.874,
                },
                "time_workload": {
                    "max": 100.0,
                    "min": 0.0,
                    "status": "ARCHETYPE",
                    "unit": "%",
                    "value": 50.0,
                },
                "units": {
                    "max": 24.0,
                    "min": 24.0,
                    "status": "ARCHETYPE",
                    "value": 24.0,
                },
                "usage_location": {
                    "status": "DEFAULT",
                    "unit": "CodSP3 - NCS Country Codes " "- NATO",
                    "value": "EEE",
                },
                "use_time_ratio": {
                    "max": 1.0,
                    "min": 1.0,
                    "status": "ARCHETYPE",
                    "unit": "/1",
                    "value": 1.0,
                },
            },
            "SSD-1": {
                "capacity": {
                    "max": 900.0,
                    "min": 900.0,
                    "status": "ARCHETYPE",
                    "unit": "GB",
                    "value": 900.0,
                },
                "density": {
                    "max": 53.6,
                    "min": 48.5,
                    "source": "Average of 3 rows",
                    "status": "COMPLETED",
                    "unit": "GB/cm2",
                    "value": 50.56666666666666,
                },
                "duration": {"unit": "hours", "value": 35040.0},
                "impacts": {
                    "adp": {
                        "description": "Use of minerals and " "fossil ressources",
                        "embedded": {
                            "max": 0.003464,
                            "min": 0.003242,
                            "value": 0.00337,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgSbeq",
                        "use": "not implemented",
                    },
                    "gwp": {
                        "description": "Total climate " "change",
                        "embedded": {
                            "max": 94.33,
                            "min": 86.56,
                            "value": 91.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "kgCO2eq",
                        "use": "not implemented",
                    },
                    "pe": {
                        "description": "Consumption of " "primary energy",
                        "embedded": {
                            "max": 1167.0,
                            "min": 1071.0,
                            "value": 1126.0,
                            "warnings": [
                                "End of life is not included in the calculation"
                            ],
                        },
                        "unit": "MJ",
                        "use": "not implemented",
                    },
                },
                "units": {"max": 4.0, "min": 4.0, "status": "ARCHETYPE", "value": 4.0},
            },
            "adp_factor": {
                "max": 2.656e-07,
                "min": 1.32e-08,
                "source": "ADEME Base IMPACTS ®",
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "value": 6.42e-08,
            },
            "avg_power": {
                "max": 354.0576,
                "min": 265.54319999999996,
                "status": "COMPLETED",
                "unit": "W",
                "value": 294.31037999999995,
            },
            "duration": {"unit": "hours", "value": 35040.0},
            "gwp_factor": {
                "max": 0.9,
                "min": 0.023,
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n"
                "Average of 27 european countries",
                "status": "DEFAULT",
                "unit": "kg CO2eq/kWh",
                "value": 0.38,
            },
            "hours_life_time": {
                "max": 35040.0,
                "min": 35040.0,
                "source": "from device",
                "status": "COMPLETED",
                "unit": "hours",
                "value": 35040.0,
            },
            "memory": {"status": "ARCHETYPE", "unit": "GB", "value": 384.0},
            "other_consumption_ratio": {
                "max": 0.6,
                "min": 0.2,
                "status": "ARCHETYPE",
                "unit": "ratio /1",
                "value": 0.33,
            },
            "pe_factor": {
                "max": 468.15,
                "min": 0.013,
                "source": "ADPf / (1-%renewable_energy)",
                "status": "DEFAULT",
                "unit": "MJ/kWh",
                "value": 12.874,
            },
            "ssd_storage": {"status": "ARCHETYPE", "unit": "GB", "value": 1800.0},
            "units": {"max": 1, "min": 1, "status": "ARCHETYPE", "value": 1},
            "usage_location": {
                "status": "DEFAULT",
                "unit": "CodSP3 - NCS Country Codes - NATO",
                "value": "EEE",
            },
            "use_time_ratio": {
                "max": 1.0,
                "min": 1.0,
                "status": "ARCHETYPE",
                "unit": "/1",
                "value": 1.0,
            },
            "vcpu": {"status": "ARCHETYPE", "value": 48.0},
        },
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_empty_usage_e8ads_v5():
    test = CloudTest(
        CloudInstanceRequest("azure", "e8ads_v5"),
        ADPImpact(
            ImpactOutput(0.02211, 0.0127, 0.0163, END_OF_LIFE_WARNING),
            ImpactOutput(0.0006984, 2.603e-05, 0.00014),
        ),
        GWPImpact(
            ImpactOutput(291.7, 108.2, 170.0, END_OF_LIFE_WARNING),
            ImpactOutput(2367.0, 45.36, 800.0),
        ),
        PEImpact(
            ImpactOutput(3713.0, 1400.0, 2200.0, END_OF_LIFE_WARNING),
            ImpactOutput(1231000.0, 25.64, 30000.0, UNCERTAINTY_WARNING),
        ),
    )

    await test.check_result()


@pytest.mark.asyncio
async def test_usage_with_complex_time_workload_e8ads_v5():
    test = CloudTest(
        CloudInstanceRequest(
            "azure",
            "e8ads_v5",
            usage={
                "time_workload": [
                    {"time_percentage": 50, "load_percentage": 0},
                    {"time_percentage": 25, "load_percentage": 60},
                    {"time_percentage": 25, "load_percentage": 100},
                ]
            },
        ),
        ADPImpact(
            ImpactOutput(0.02211, 0.0127, 0.0163, END_OF_LIFE_WARNING),
            ImpactOutput(0.0006088, 2.269e-05, 0.00012),
        ),
        GWPImpact(
            ImpactOutput(291.7, 108.2, 170.0, END_OF_LIFE_WARNING),
            ImpactOutput(2063.0, 39.54, 700.0),
        ),
        PEImpact(
            ImpactOutput(3713.0, 1400.0, 2200.0, END_OF_LIFE_WARNING),
            ImpactOutput(1073000.0, 22.35, 20000.0, UNCERTAINTY_WARNING),
        ),
    )

    await test.check_result()
