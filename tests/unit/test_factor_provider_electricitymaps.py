from unittest.mock import MagicMock, patch

import pytest

from boaviztapi.service.factor_provider import (
    get_electrical_impact_factor,
    get_electrical_min_max,
)


class TestGetElectricalImpactFactorElectricitymaps:
    @patch("boaviztapi.service.factor_provider.config")
    @patch("boaviztapi.service.electricitymaps._cache", {})
    @patch("boaviztapi.service.electricitymaps.create_client")
    def test_gwp_success(self, mock_create_client, mock_config):
        mock_config.electricity_maps_api_key = "test-key"

        mock_response = MagicMock()
        mock_response.carbon_intensity = 80.0
        mock_client = MagicMock()
        mock_client.carbon_intensity.latest.return_value = mock_response
        mock_create_client.return_value = mock_client

        result = get_electrical_impact_factor("FRA", "gwp")

        assert result["value"] == pytest.approx(0.08)
        assert result["unit"] == "kg CO2eq/kWh"
        assert result["source"] == "Electricity Maps API (lifecycle)"

    @patch("boaviztapi.service.factor_provider.config")
    def test_non_gwp_falls_back_to_hardcoded(self, mock_config):
        mock_config.electricity_maps_api_key = "test-key"

        result = get_electrical_impact_factor("FRA", "pe")

        assert result["value"] == pytest.approx(11.289)
        assert result["unit"] == "MJ"


class TestGetElectricalImpactFactorHardcoded:
    @patch("boaviztapi.service.factor_provider.config")
    def test_hardcoded_returns_factors_yml_data(self, mock_config):
        mock_config.electricity_maps_api_key = None

        result = get_electrical_impact_factor("FRA", "gwp")

        assert result["value"] == pytest.approx(0.098)

    @patch("boaviztapi.service.factor_provider.config")
    def test_hardcoded_unknown_location_raises(self, mock_config):
        mock_config.electricity_maps_api_key = None

        with pytest.raises(NotImplementedError):
            get_electrical_impact_factor("NONEXISTENT", "gwp")


class TestGetElectricalMinMaxElectricitymaps:
    @patch("boaviztapi.service.factor_provider.config")
    def test_gwp_returns_hardcoded_bounds(self, mock_config):
        mock_config.electricity_maps_api_key = "test-key"

        result = get_electrical_min_max("gwp", "min")

        assert isinstance(result, float)

    @patch("boaviztapi.service.factor_provider.config")
    def test_non_gwp_returns_hardcoded_bounds(self, mock_config):
        mock_config.electricity_maps_api_key = "test-key"

        result = get_electrical_min_max("pe", "min")

        assert result == pytest.approx(0.013)
