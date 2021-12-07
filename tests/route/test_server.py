from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_complete_cpu():
    res = client.post('/v1/component/cpu', data={
        "units": 2,
        "core_units": 24,
        "die_size_per_core": 0.245
    })

    assert True


def test_complete_server():
    res = client.post('/v1/server/bottom-up', data={
        "model": {
        },
        "configuration": {
            "cpu": {
                "units": 2,
                "core_units": 24,
                "die_size": 0.245,
            },
            "ram": [
                {
                    "units": 4,
                    "capacity": 32,
                    "density": 1.79,
                },
                {
                    "units": 4,
                    "capacity": 16,
                    "density": 1.79,
                }
            ],
            "disk": [
                {
                    "units": 2,
                    "type": "ssd",
                    "capacity": 400,
                    "density": 50.6,
                },
                {
                    "units": 2,
                    "type": "hdd",
                }
            ],
            "power_supply": {
                "units": 2,
                "unit_weight": 10
            }
        }
    })
    assert True


def test_empty_config_server():
    res = client.post('/v1/server/bottom-up', data={
        "model": {
        },
        "configuration": {
        }
    })
    assert True


def test_partial_server_1():
    res = client.post('/v1/server/bottom-up', data={
        "model": {
        },
        "configuration": {
            "cpu": {
                "units": 2,
            },
            "ram": [
                {
                    "units": 4,
                    "capacity": 32,
                },
                {
                    "units": 4,
                    "capacity": 16,
                }
            ],
            "disk": [
                {
                    "units": 2,
                    "type": "ssd",
                },
                {
                    "units": 2,
                    "type": "hdd",
                }
            ]
        }
    })
    assert True


def test_partial_server_2():
    res = client.post('/v1/server/bottom-up', data={
        "model": {
        },
        "configuration": {
            "cpu": {
                "units": 2,
                "die_size": 0.245,
            },
            "ram": [
                {
                    "units": 4,
                },
                {
                    "units": 4,
                    "capacity": 16,
                    "density": 1.79,

                }
            ],
            "disk": [
                {
                    "units": 2,
                    "capacity": 400,
                    "density": 50.6,
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
    assert True