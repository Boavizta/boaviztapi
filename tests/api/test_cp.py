import pytest

from httpx import AsyncClient, ASGITransport
from dataclasses import dataclass
from typing import Optional, Tuple

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


@dataclass
class CPUConsumptionProfileTest:
    name: str
    expected: Tuple[float, float, float, float]

    tdp: Optional[int] = None

    async def run(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            request_body = {"cpu": {"name": self.name}}
            if self.tdp:
                request_body["cpu"]["tdp"] = self.tdp

            res = await ac.post("/v1/consumption_profile/cpu", json=request_body)

        res_data: dict = res.json()
        delta = 0.01
        assert self.expected[0] == pytest.approx(res_data["a"], delta)
        assert self.expected[1] == pytest.approx(res_data["b"], delta)
        assert self.expected[2] == pytest.approx(res_data["c"], delta)
        assert self.expected[3] == pytest.approx(res_data["d"], delta)

@pytest.mark.asyncio
async def test_complete_valid_cpu_manufacturer_family_partial():
    await CPUConsumptionProfileTest(name="intel xeon", expected=(15.7628, 0.07359, 20.4511, -2.7476)).run()

@pytest.mark.asyncio
async def test_complete_valid_cpu_manufacturer_family():
    await CPUConsumptionProfileTest(name="intel xeon gold 6134", expected=(35.5688, 0.2438, 9.6694, -0.6087)).run()

@pytest.mark.asyncio
async def test_complete_valid_cpu_overrides_tdp_if_present():
    await CPUConsumptionProfileTest(name="intel xeon gold 6134", tdp=100, expected=(50.8479, 0.0630, 20.4511, -0.9999)).run()

@pytest.mark.asyncio
async def test_complete_alternative_valid_cpu_manufacturer_family():
    await CPUConsumptionProfileTest(name="amd epyc 7251", expected=(61.0175, 0.0677, 20.4511, -5.5482)).run()

@pytest.mark.asyncio
async def test_complete_invalid_cpu_returns_default():
    await CPUConsumptionProfileTest(name="foobar", expected=(171.1813, 0.0354, 36.89, -10.13)).run()
