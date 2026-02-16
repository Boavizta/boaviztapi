from unittest.mock import MagicMock, patch

import pytest
from openapi.exceptions import ApiException

from boaviztapi.service.electricitymaps import fetch_carbon_intensity


class TestFetchCarbonIntensity:
    @patch("boaviztapi.service.electricitymaps._cache", {})
    @patch("boaviztapi.service.electricitymaps.create_client")
    def test_success(self, mock_create_client):
        mock_response = MagicMock()
        mock_response.carbon_intensity = 52.0
        mock_client = MagicMock()
        mock_client.carbon_intensity.latest.return_value = mock_response
        mock_create_client.return_value = mock_client

        result = fetch_carbon_intensity("test-key", "FR")

        assert result["unit"] == "kg CO2eq/kWh"
        assert result["source"] == "Electricity Maps API (lifecycle)"
        assert result["value"] == pytest.approx(0.052)
        assert result["min"] == pytest.approx(0.052)
        assert result["max"] == pytest.approx(0.052)

        mock_create_client.assert_called_once_with(api_key="test-key")
        mock_client.carbon_intensity.latest.assert_called_once_with(zone_key="FR")

    @patch("boaviztapi.service.electricitymaps._cache", {})
    @patch("boaviztapi.service.electricitymaps.create_client")
    def test_api_error(self, mock_create_client):
        mock_client = MagicMock()
        mock_client.carbon_intensity.latest.side_effect = ApiException(
            status=500, reason="Server Error"
        )
        mock_create_client.return_value = mock_client

        with pytest.raises(ConnectionError, match="request failed"):
            fetch_carbon_intensity("test-key", "FR")

    @patch("boaviztapi.service.electricitymaps._cache", {})
    @patch("boaviztapi.service.electricitymaps.create_client")
    def test_auth_error(self, mock_create_client):
        mock_client = MagicMock()
        mock_client.carbon_intensity.latest.side_effect = ApiException(
            status=403, reason="Forbidden"
        )
        mock_create_client.return_value = mock_client

        with pytest.raises(ConnectionError, match="request failed"):
            fetch_carbon_intensity("test-key", "FR")

    @patch("boaviztapi.service.electricitymaps._cache", {})
    @patch("boaviztapi.service.electricitymaps.create_client")
    def test_cached_result_skips_api_call(self, mock_create_client):
        mock_response = MagicMock()
        mock_response.carbon_intensity = 52.0
        mock_client = MagicMock()
        mock_client.carbon_intensity.latest.return_value = mock_response
        mock_create_client.return_value = mock_client

        result1 = fetch_carbon_intensity("test-key", "FR")
        result2 = fetch_carbon_intensity("test-key", "FR")

        assert result1 == result2
        mock_client.carbon_intensity.latest.assert_called_once()
