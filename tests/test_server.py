from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_complete_config_server():
    res = client.post('/v1/server/bottom-up?verbose=false', json={
        "model": {
        },
        "configuration": {
            "cpu": {
                "units": 2,
                "core_units": 24,
                "die_size": 0.245
            },
            "ram": [
                {
                    "units": 4,
                    "capacity": 32,
                    "density": 1.79
                },
                {
                    "units": 4,
                    "capacity": 16,
                    "density": 1.79
                }
            ],
            "disk": [
                {
                    "units": 2,
                    "type": "ssd",
                    "capacity": 400,
                    "density": 50.6
                },
                {
                    "units": 2,
                    "type": "hdd"
                }
            ],
            "power_supply": {
                "units": 2,
                "unit_weight": 10
            }
        }
    })
    assert res.json() == {
        "gwp": 1117.0,
        "pe": 15153.0,
        "adp": 0.254
    }


def test_empty_config_server():
    res = client.post('/v1/server/bottom-up?verbose=false', json={
    })
    assert res.json() == {
        "gwp": 3292.0,
        "pe": 41821.0,
        "adp": 0.234
    }


def test_dell_r740_server():
    res = client.post('/v1/server/bottom-up?verbose=false', json={
        "model":
            {
                "manufacturer": "Dell",
                "name": "R740",
                "type": "rack",
                "year": 2020
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
            }
    })
    assert res.json() == {
        "gwp": 970.0,
        "pe": 12896.0,
        "adp": 0.149
    }


def test_partial_server_1():
    res = client.post('/v1/server/bottom-up?verbose=false', json={
        "model": {
        },
        "configuration": {
            "cpu": {
                "units": 2
            },
            "ram": [
                {
                    "units": 4,
                    "capacity": 32
                },
                {
                    "units": 4,
                    "capacity": 16
                }
            ],
            "disk": [
                {
                    "units": 2,
                    "type": "ssd"
                },
                {
                    "units": 2,
                    "type": "hdd"
                }
            ]
        }
    })
    assert res.json() == {
        "gwp": 1295.0,
        "pe": 16669.0,
        "adp": 0.151
    }


def test_partial_server_2():
    res = client.post('/v1/server/bottom-up?verbose=false', json={
        "model": {
        },
        "configuration": {
            "cpu": {
                "units": 2,
                "die_size": 0.245
            },
            "ram": [
                {
                    "units": 4
                },
                {
                    "units": 4,
                    "capacity": 16,
                    "density": 1.79

                }
            ],
            "disk": [
                {
                    "units": 2,
                    "capacity": 400,
                    "density": 50.6
                },
                {
                    "units": 2
                }
            ],
            "power_supply": {
                "units": 2,
                "unit_weight": 10
            }
        }
    })
    assert res.json() == {
        "gwp": 1323.0,
        "pe": 17953.0,
        "adp": 0.259
    }


def test_partial_server_3():
    res = client.post('/v1/server/bottom-up?verbose=false', json={
        "model": {
        },
        "configuration": {

            "ram": [
                {
                    "units": 4,
                    "capacity": 16,
                    "density": 1.79

                }
            ],
            "power_supply": {
                "units": 2,
                "unit_weight": 10
            }
        }
    })
    assert res.json() == {
        "gwp": 903.0,
        "pe": 12706.0,
        "adp": 0.242
    }
