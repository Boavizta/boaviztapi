import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_complete_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?instance_type=a1.4xlarge&verbose=false', json={
            "hours_use_time": 2,
            "usage_location": "FRA",
            "workload": {
                "10": {
                    "time": 0
                },
                "50": {
                    "time": 1
                },
                "100": {
                    "time": 0
                },
                "idle": {
                    "time": 0
                }
            }
        })

    assert res.json() == {
        "gwp": {
            "manufacture": 565.0,
            "use": 0.00560505  # no rounding until #43 isn't implemented

        },
        "pe": {
            "manufacture": 7720.0,
            "use": "Not Implemented"
        },
        "adp": {
            "manufacture": 0.102,
            "use": "Not Implemented"
        }
    }

@pytest.mark.asyncio
async def test_default_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?instance_type=a1.4xlarge&verbose=false', json={
        })

    assert res.json() == {
        "gwp": {
            "manufacture": 565.0,
            "use": 100.8786708  # no rounding until #43 isn't implemented
        },
        "pe": {
            "manufacture": 7720.0,
            "use": "Not Implemented"
        },
        "adp": {
            "manufacture": 0.102,
            "use": "Not Implemented"
        }
    }
