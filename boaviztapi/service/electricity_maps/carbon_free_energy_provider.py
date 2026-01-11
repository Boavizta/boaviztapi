from datetime import datetime, timedelta

from boaviztapi.service.cache.cache import CacheService
from boaviztapi.service.electricity_maps.costs_provider import ElectricityCostsProvider
from boaviztapi.service.electricitymaps_service import ElectricityMapsService
from boaviztapi.service.utils import temporal_granularity_to_ttl


class CarbonFreeEnergyProvider(ElectricityMapsService):

    @staticmethod
    def get_cache_scheduler(temporalGranularity: str = 'hourly') -> CacheService:
        endpoints = []
        if temporalGranularity.lower() in ['15_minutes', 'hourly']:
            for country in ElectricityCostsProvider.get_eic_countries():
                url = f"{ElectricityMapsService.base_url}/carbon-free-energy/latest?zone={country.zone_code}&temporalGranularity={temporalGranularity}"
                endpoints.append(url)
        elif temporalGranularity.lower() in ['daily', 'monthly', 'quarterly', 'yearly']:
            datetime_parameter = (datetime.now() - timedelta(
                seconds=temporal_granularity_to_ttl(temporalGranularity))).strftime(
                "%Y-%m-%dT%H:%M:00Z")
            for country in ElectricityCostsProvider.get_eic_countries():
                url = f"{ElectricityMapsService.base_url}/carbon-free-energy/past?zone={country.zone_code}&datetime={datetime_parameter}&temporalGranularity={temporalGranularity}"
                endpoints.append(url)
        api_token = ElectricityMapsService._get_api_key()
        cache_service = CacheService(name=f"electricity_carbon_free_energy_cache_{temporalGranularity}",
                                     endpoints=endpoints,
                                     ttl=temporal_granularity_to_ttl(temporalGranularity),
                                     headers={"auth-token": api_token})
        return cache_service