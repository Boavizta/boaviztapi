import pytest

from boaviztapi import config
from boaviztapi.service.factor_provider import get_electrical_impact_factor

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not config.electricity_maps_api_key,
        reason="Electricity Maps API key not set",
    ),
]


class TestGetElectricalImpactFactor:
    def test_returns_gwp_factor_for_known_country(self):
        result = get_electrical_impact_factor("FRA", "gwp")

        assert result["unit"] == "kg CO2eq/kWh"
        assert result["source"] == "Electricity Maps API (lifecycle)"
        assert isinstance(result["value"], float)
        assert result["value"] > 0
        assert result["min"] == result["value"]
        assert result["max"] == result["value"]

    def test_non_gwp_falls_back_to_hardcoded(self):
        result = get_electrical_impact_factor("FRA", "pe")

        assert result["value"] == 11.289
        assert result["source"] == "ADPf / (1-%renewable_energy)"

    def test_world_location_falls_back_to_hardcoded(self):
        result = get_electrical_impact_factor("WOR", "gwp")

        assert result["value"] == 0.39
        assert result["source"] == "Average of all country in the csv"

    def test_unknown_country_falls_back_to_not_implemented(self):
        with pytest.raises(NotImplementedError):
            get_electrical_impact_factor("ZZZ", "gwp")
