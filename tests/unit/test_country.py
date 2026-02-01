import pytest

from boaviztapi.utils.country import iso3_to_iso2


class TestIso3ToIso2:
    def test_fra_to_fr(self):
        assert iso3_to_iso2("FRA") == "FR"

    def test_deu_to_de(self):
        assert iso3_to_iso2("DEU") == "DE"

    def test_usa_to_us(self):
        assert iso3_to_iso2("USA") == "US"

    def test_wor_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown ISO3 country code: 'WOR'"):
            iso3_to_iso2("WOR")

    def test_unknown_code_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown ISO3 country code: 'XYZ'"):
            iso3_to_iso2("XYZ")
