import pytest
from httpx import AsyncClient

from boaviztapi.main import app

from dataclasses import dataclass
from .util import (
    InstanceRequest,
    AdpImpact,
    GwpImpact,
    PeImpact,
    ImpactOutput,
    END_OF_LIFE_WARNING,
    UNCERTAINTY_WARNING,
)

pytest_plugins = ("pytest_asyncio",)


@dataclass
class CloudTest:
    request: InstanceRequest

    adp: AdpImpact
    gwp: GwpImpact
    pe: PeImpact

    use_url_params: bool = False

    async def check_result(self):
        if self.use_url_params:
            url = f"/v1/cloud/instance?verbose=false&instance_type={self.instance_type}&provider={self.provider}"
        else:
            url = "/v1/cloud/instance?verbose=false"

        async with AsyncClient(app=app, base_url="http://test") as ac:
            res = await ac.post(
                url,
                json=None if self.use_url_params else self.request.to_dict(),
            )

        assert res.json() == {
            "impacts": {
                "adp": self.adp.to_dict(),
                "gwp": self.gwp.to_dict(),
                "pe": self.pe.to_dict(),
            },
        }


@pytest.mark.asyncio
async def test_empty_usage():
    test = CloudTest(
        InstanceRequest("aws", "a1.4xlarge", {}),
        AdpImpact(
            ImpactOutput(0.1414, 0.06512, 0.099, END_OF_LIFE_WARNING),
            ImpactOutput(0.000581, 2.165e-05, 0.00012),
        ),
        GwpImpact(
            ImpactOutput(636.6, 258.9, 450.0, END_OF_LIFE_WARNING),
            ImpactOutput(1969.0, 37.73, 700.0),
        ),
        PeImpact(
            ImpactOutput(8846.0, 3542.0, 6300.0, END_OF_LIFE_WARNING),
            ImpactOutput(1024000.0, 21.33, 20000.0, UNCERTAINTY_WARNING),
        ),
    )

    test.check_result()


@pytest.mark.asyncio
async def test_empty_usage_m6gxlarge():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false",
            json={"provider": "aws", "instance_type": "m6g.xlarge", "usage": {}},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.01088,
                    "min": 0.005075,
                    "value": 0.0075,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.0001721, "min": 6.415e-06, "value": 3e-05},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 89.23,
                    "min": 31.58,
                    "value": 55.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 583.2, "min": 11.18, "value": 200.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 1168.0,
                    "min": 416.4,
                    "value": 730.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 303400.0, "min": 6.318, "value": 10000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get(
            "/v1/cloud/instance?verbose=false&instance_type=a1.2xlarge&provider=aws"
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.07069,
                    "min": 0.03256,
                    "value": 0.049,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.0002905, "min": 1.083e-05, "value": 6e-05},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 318.3,
                    "min": 129.5,
                    "value": 230.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 984.3, "min": 18.87, "value": 350.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 4423.0,
                    "min": 1771.0,
                    "value": 3200.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 512000.0, "min": 10.66, "value": 10000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get(
            "/v1/cloud/instance?verbose=false&instance_type=r5ad.12xlarge&provider=aws"
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.1206,
                    "min": 0.06419,
                    "value": 0.086,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.003295, "min": 0.0001228, "value": 0.0007},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 1694.0,
                    "min": 593.4,
                    "value": 1000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 11170.0, "min": 214.0, "value": 4000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 21480.0,
                    "min": 7606.0,
                    "value": 13000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 5808000.0, "min": 121.0, "value": 100000.0},
            },
        }
    }


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
async def test_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false",
            json={
                "provider": "aws",
                "instance_type": "c5a.24xlarge",
                "usage": {
                    "time_workload": [
                        {"time_percentage": 50, "load_percentage": 0},
                        {"time_percentage": 25, "load_percentage": 60},
                        {"time_percentage": 25, "load_percentage": 100},
                    ]
                },
            },
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.1744,
                    "min": 0.08627,
                    "value": 0.124,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.002975, "min": 0.0001109, "value": 0.0006},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 1216.0,
                    "min": 459.3,
                    "value": 780.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 10080.0, "min": 193.2, "value": 3500.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 16090.0,
                    "min": 6121.0,
                    "value": 10500.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 5244000.0, "min": 109.2, "value": 100000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false",
            json={
                "provider": "aws",
                "instance_type": "c5a.24xlarge",
                "usage": {"time_workload": 100},
            },
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.1744,
                    "min": 0.08627,
                    "value": 0.124,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.005068, "min": 0.0001889, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 1216.0,
                    "min": 459.3,
                    "value": 780.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 17170.0, "min": 329.2, "value": 6000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 16090.0,
                    "min": 6121.0,
                    "value": 10500.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 8934000.0, "min": 186.1, "value": 200000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false&duration=1",
            json={"provider": "aws", "instance_type": "c5a.24xlarge", "usage": {}},
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 4.977e-06,
                    "min": 2.462e-06,
                    "value": 3.5e-06,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 1.122e-07, "min": 4.182e-09, "value": 2e-08},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 0.0347,
                    "min": 0.01311,
                    "value": 0.022,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 0.3802, "min": 0.007287, "value": 0.13},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 0.4591,
                    "min": 0.1747,
                    "value": 0.3,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 197.8,
                    "min": 0.004119,
                    "value": 5.0,
                    "warnings": [
                        "Uncertainty from technical characteristics is very important. Results should be "
                        "interpreted with caution (see min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false&duration=2",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {
                    "usage_location": "FRA",
                    "time_workload": [
                        {"time_percentage": "50", "load_percentage": "0"},
                        {"time_percentage": "50", "load_percentage": "50"},
                    ],
                },
            },
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 8.07e-06,
                    "min": 3.717e-06,
                    "value": 5.6e-06,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 4.11e-09, "min": 3.082e-09, "value": 3.4e-09},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 0.03634,
                    "min": 0.01478,
                    "value": 0.026,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 0.008291, "min": 0.006218, "value": 0.0069},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 0.5049,
                    "min": 0.2022,
                    "value": 0.36,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 0.955, "min": 0.7163, "value": 0.79},
            },
        }
    }


@pytest.mark.asyncio
async def test_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get(
            "/v1/cloud/instance?verbose=true&instance_type=r5ad.12xlarge&provider=aws"
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.1206,
                    "min": 0.06419,
                    "value": 0.086,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.003295, "min": 0.0001228, "value": 0.0007},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 1694.0,
                    "min": 593.4,
                    "value": 1000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 11170.0, "min": 214.0, "value": 4000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 21480.0,
                    "min": 7606.0,
                    "value": 13000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 5808000.0, "min": 121.0, "value": 100000.0},
            },
        },
        "verbose": {
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
    }
