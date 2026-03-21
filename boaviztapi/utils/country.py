import pycountry


def is_iso3(iso3_code: str) -> bool:
    """Checks whether country code is present in ISO 3166-1 alpha-3 country list."""
    return pycountry.countries.get(alpha_3=iso3_code) is not None


def iso3_to_iso2(iso3_code: str) -> str:
    """Convert an ISO 3166-1 alpha-3 country code to alpha-2."""
    country = pycountry.countries.get(alpha_3=iso3_code)
    if country is None:
        raise ValueError(f"Unknown ISO3 country code: '{iso3_code}'")

    return country.alpha_2
