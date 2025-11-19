from boaviztapi.service.cache.cache import CacheService
from boaviztapi.service.costs_provider import ElectricityCostsProvider
from boaviztapi.service.electricitymaps_service import ElectricityMapsService


class CarbonIntensityProvider(ElectricityMapsService):

    @staticmethod
    def get_carbon_intensity(zone: str, temporalGranularity: str = 'hourly'):
        url = f"{ElectricityMapsService.base_url}/carbon-intensity/latest?zone={zone}&temporalGranularity={temporalGranularity}"
        return ElectricityMapsService._perform_request(url)

    @staticmethod
    def get_power_breakdown(zone: str, temporalGranularity: str = 'hourly'):
        url = f"{ElectricityMapsService.base_url}/power-breakdown/latest?zone={zone}&temporalGranularity={temporalGranularity}"
        return ElectricityMapsService._perform_request(url)

    @staticmethod
    def get_cache_scheduler(temporalGranularity: str = 'hourly') -> CacheService:
        endpoints = []
        for country in ElectricityCostsProvider.get_eic_countries():
            url = f"{ElectricityMapsService.base_url}/power-breakdown/latest?zone={country.zone_code}&temporalGranularity={temporalGranularity}"
            endpoints.append(url)
        # TODO: Add temporal granularity as an environment variable, or make it configurable during runtime
        api_token = ElectricityMapsService._get_api_key()
        return CacheService(name="electricity_power_breakdown_cache", endpoints=endpoints, ttl=3600,
                            headers={"auth-token": api_token})