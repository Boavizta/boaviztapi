import pytest

from boaviztapi.service.factor_provider import (
    get_electrical_impact_factor,
    get_electrical_min_max,
)


class TestWuElectricityFactors:
    """Test that wu (water use) electricity impact factors are available for countries with data."""

    @pytest.mark.parametrize(
        "country_code,expected_value",
        [
            ("FRA", 0.0036736961),
            ("USA", 0.003132125),
            ("DEU", 0.001946974),
            ("JPN", 0.0023063545),
            ("BRA", 0.018603389),
        ],
    )
    def test_wu_factor_available_for_known_countries(
        self, country_code, expected_value
    ):
        factor = get_electrical_impact_factor(country_code, "wu")
        assert factor["value"] == expected_value
        assert factor["unit"] == "m3/kWh"
        assert "wri.org" in factor["source"]

    def test_wu_factor_not_available_for_countries_without_data(self):
        with pytest.raises(NotImplementedError):
            get_electrical_impact_factor("WOR", "wu")

    def test_wu_factor_not_available_for_country_without_wu(self):
        with pytest.raises(NotImplementedError):
            get_electrical_impact_factor("AGO", "wu")

    def test_wu_min_max(self):
        assert get_electrical_min_max("wu", "min") == 0.0011184881
        assert get_electrical_min_max("wu", "max") == 0.018603389
