from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_complete_cpu():
    res = client.post('/v1/component/cpu?verbose=false', json={
        "core_units": 12,
        "die_size_per_core": 0.245
    })

    assert res.json() == {
        "gwp": {
            "manufacture": 16.0,
            "use": "not implemented"
        },
        "pe": {
            "manufacture": 247.0,
            "use": "not implemented"
        },
        "adp": {
            "manufacture": 0.02,
            "use": "not implemented"
        }
    }


def test_empty_cpu():
    res = client.post('/v1/component/cpu?verbose=false', json={
    })

    assert res.json() == {
        "gwp": {
            "manufacture": 22.0,
            "use": "not implemented"
        },
        "pe": {
            "manufacture": 325.0,
            "use": "not implemented"
        },
        "adp": {
            "manufacture": 0.02,
            "use": "not implemented"
        }
    }


def test_complete_ram():
    res = client.post('/v1/component/ram?verbose=false', json={
        "units": 12,
        "capacity": 32,
        "density": 1.79
    })

    assert res.json() == {
        "gwp": {
            "manufacture": 45.0,
            "use": "not implemented"
        },
        "pe": {
            "manufacture": 562.0,
            "use": "not implemented"
        },
        "adp": {
            "manufacture": 0.003,
            "use": "not implemented"
        }
    }


def test_empty_ram():
    res = client.post('/v1/component/ram?verbose=false', json={
    })

    assert res.json() == {
        "gwp": {
            "manufacture": 118.0,
            "use": "not implemented"
        },
        "pe": {
            "manufacture": 1472.0,
            "use": "not implemented"
        },
        "adp": {
            "manufacture": 0.005,
            "use": "not implemented"
        }
    }


def test_complete_ssd():
    res = client.post('/v1/component/ssd?verbose=false', json={
        "capacity": 400,
        "density": 50.6
    })

    assert res.json() == {
        "gwp": {
            "manufacture": 24.0,
            "use": "not implemented"
        },
        "pe": {
            "manufacture": 293.0,
            "use": "not implemented"
        },
        "adp": {
            "manufacture": 0.001,
            "use": "not implemented"
        },
    }


def test_empty_ssd():
    res = client.post('/v1/component/ssd?verbose=false', json={
    })

    assert res.json() == {
        "gwp": {
            "manufacture": 52.0,
            "use": "not implemented"
        },
        "pe": {
            "manufacture": 640.0,
            "use": "not implemented"
        },
        "adp": {
            "manufacture": 0.002,
            "use": "not implemented"
        },
    }
