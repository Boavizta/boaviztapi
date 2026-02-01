import time

from electricitymaps import create_client
from openapi.exceptions import ApiException

from boaviztapi.utils.config import config

_cache: dict[str, tuple[float, dict]] = {}


def fetch_carbon_intensity(api_key: str, zone: str) -> dict:
    """Fetch real-time carbon intensity from the Electricity Maps API.

    Returns a dict matching the factor format used by factors.yml::

        {
            "unit": "kg CO2eq/kWh",
            "source": "Electricity Maps API (lifecycle)",
            "value": <carbonIntensity / 1000>,
            "min": <carbonIntensity / 1000>,
            "max": <carbonIntensity / 1000>,
        }

    Raises ConnectionError on request failure.
    """
    cached = _cache.get(zone)
    if cached is not None:
        ts, result = cached
        if time.monotonic() - ts < config.electricity_maps_cache_expiry_seconds:
            return result

    client = create_client(api_key=api_key)

    try:
        response = client.carbon_intensity.latest(zone_key=zone)
    except ApiException as exc:
        raise ConnectionError(f"Electricity Maps API request failed: {exc}") from exc

    value = response.carbon_intensity / 1000

    result = {
        "unit": "kg CO2eq/kWh",
        "source": "Electricity Maps API (lifecycle)",
        "value": value,
        "min": value,
        "max": value,
    }

    _cache[zone] = (time.monotonic(), result)

    return result
