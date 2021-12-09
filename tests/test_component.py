from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_complete_cpu():
    res = client.post('/v1/component/cpu', json={
        "core_units": 12,
        "die_size_per_core": 0.245
    })

    assert res, {
        "gwp": 16.0,
        "pe": 247.0,
        "adp": 0.02
    }


def test_empty_cpu():
    res = client.post('/v1/component/cpu', json={
    })

    assert res, {
        "gwp": 22.0,
        "pe": 325.0,
        "adp": 0.02
    }


def test_complete_ram():
    res = client.post('/v1/component/ram', json={
        "units": 12,
        "capacity": 32,
        "density": 1.79
    })

    assert res, {
        "gwp": 45.0,
        "pe": 562.0,
        "adp": 0.003
    }


def test_empty_ram():
    res = client.post('/v1/component/ram', json={
    })

    assert res, {
        "gwp": 118.0,
        "pe": 1472.0,
        "adp": 0.005
    }


def test_complete_ssd():
    res = client.post('/v1/component/ssd', json={
        "units": 12,
        "capacity": 32,
        "density": 1.79
    })

    assert res, {
        "gwp": 24.0,
        "pe": 293.0,
        "adp": 0.001
    }


def test_empty_ssd():
    res = client.post('/v1/component/ssd', json={
    })

    assert res, {
        "gwp": 52.0,
        "pe": 640.0,
        "adp": 0.002
    }
