import logging
from unittest.mock import AsyncMock

logging.basicConfig(level=logging.DEBUG)


class DummyCtx:
    def __init__(self):
        self.ELECTRICITYMAPS_API_KEY = "DUMMY"
        self.ENTSOE_API_KEY = "DUMMY"
        self.GOOGLE_CLIENT_ID = "DUMMY"
        self.GOOGLE_CLIENT_SECRET = "DUMMY"
        self.SESSION_MIDDLEWARE_SECRET_KEY = "DUMMY"
        self.mongodb_client = AsyncMock()
        self.database_name = "testdb"

    def load_secrets(self):
        return None

    async def create_db_connection(self):
        return None

    async def close_db_connection(self):
        return None


def pytest_configure(config):
    for arg in config.args:
        if "test_cache.py" in str(arg):
            logging.debug("pytest_configure: skipping patches for caching tests")
            return  # Do not apply patches when running caching tests
    logging.debug("pytest_configure: applying patches before test imports")

    # Patch get_app_context in application_context module
    import boaviztapi.application_context as ctx_mod
    ctx_mod.get_app_context = lambda: DummyCtx()

    # Prevent CacheService.startup from performing network or DB operations during app lifespan
    async def _noop_startup(self):
        return None

    import boaviztapi.service.cache.cache as cache_mod
    cache_mod.CacheService.startup = _noop_startup

    # Patch electricity and carbon providers to return deterministic sample data
    import boaviztapi.service.electricity_maps.costs_provider as costs_mod
    import boaviztapi.service.electricity_maps.carbon_intensity_provider as carbon_mod

    async def _fake_price(zone: str, temporalGranularity: str = 'hourly'):
        return {
            "zone": zone,
            "datetime": "2025-11-19T20:00:00.000Z",
            "createdAt": "2025-11-18T12:21:16.175Z",
            "updatedAt": "2025-11-18T12:21:16.175Z",
            "value": 124.81,
            "unit": "EUR/MWh",
            "source": "nordpool.com",
            "temporalGranularity": temporalGranularity,
        }

    def _fake_carbon(zone: str, temporalGranularity: str = 'hourly'):
        return {
            "zone": zone,
            "carbonIntensity": 200.5,
            "datetime": "2025-11-19T20:00:00.000Z",
            "updatedAt": "2025-11-19T19:26:32.561Z",
            "createdAt": "2025-11-19T13:25:30.600Z",
            "emissionFactorType": "CO2",
            "isEstimated": True,
            "estimationMethod": "GENERAL",
            "temporalGranularity": temporalGranularity,
        }

    def _fake_power_breakdown(zone: str, temporalGranularity: str = 'hourly'):
        return {"zone": zone, "temporalGranularity": temporalGranularity, "powerProductionBreakdown": {}}

    costs_mod.ElectricityCostsProvider.get_price_for_country_elecmaps = _fake_price
    carbon_mod.CarbonIntensityProvider.get_carbon_intensity = _fake_carbon
    carbon_mod.CarbonIntensityProvider.get_power_breakdown = _fake_power_breakdown
