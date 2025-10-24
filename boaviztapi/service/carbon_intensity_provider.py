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