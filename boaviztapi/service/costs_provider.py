import logging
import os
from datetime import datetime, timezone, timedelta

import pandas as pd
import requests
import xmltodict

from boaviztapi import data_dir
from boaviztapi.application_context import get_app_context
from boaviztapi.dto.electricity.electricity import Country
from boaviztapi.service.cache.cache import CacheService
from boaviztapi.service.electricitymaps_service import ElectricityMapsService
from boaviztapi.service.exceptions import APIError, APIAuthenticationError, APIMissingValueError, \
    APIResponseParsingError

_logger = logging.getLogger(__name__)

df = pd.read_csv(os.path.join(data_dir, 'electricity/electricity_zones.csv'))
df.fillna(value='', inplace=True)

class ElectricityCostsProvider(ElectricityMapsService):
    """
    Provides functionality to retrieve and process electricity-costs-related data from one or more external APIs.
    """
    @staticmethod
    def get_eic_countries() -> list[Country]:
        """
        Get the list of EIC codes and their countries and return it as a dict
        """
        records = df.to_dict(orient='records')
        return [Country(**record) for record in records]

    @staticmethod
    def get_EIC_for_country(iso3_country: str) -> str:
        """
        Get the EIC code for a country.
        """
        return df.query(f"alpha_3 == '{iso3_country}' ")["EIC_code"].iloc[0]

    @staticmethod
    async def get_price_for_country_elecmaps(zone: str, temporalGranularity: str = 'hourly') -> dict | None:
        """
        Get the latest electricity price for a country using the ElectricityMaps API.

        Args:
            zone: Zone code as defined in the ElectricityMaps API
            temporalGranularity: The temporal granularity of the price data. Defaults to hourly.

        Returns:
            A JSON response from the ElectricityMaps API

        Raises:
            APIAuthenticationError: When the API key is not authorized to access this resource
            APIError: When the API returns an unexpected response status code, or it cannot be reached
        """
        if temporalGranularity.lower() != 'hourly':
            raise APIError("Please use the /prices endpoint for other temporal granularity parameters than 'hourly'.")
        url = f"{ElectricityMapsService.base_url}/price-day-ahead/latest?zone={zone}&temporalGranularity={temporalGranularity}"
        cached_results = await ElectricityCostsProvider.get_cache_scheduler(temporalGranularity).get_results()
        if cached_results and url in cached_results:
            return cached_results[url]

        return ElectricityMapsService._perform_request(url)

    @staticmethod
    def get_price_for_country(alpha3: str) -> dict | None:
        """
        Get a timeseries of electricity prices for a country. The default granularity is hourly.

        Args:
            alpha3: ISO 3166-1 alpha-3 country code

        Returns:
            An XML response from the ENTSO-E API, converted to a Python dictionary

        Raises:
            APIAuthenticationError: When no ENTSOE API key is found in the application context
            APIError: When the API returns an unexpected response status code
        """
        ctx = get_app_context()
        security_token = ctx.ENTSOE_API_KEY
        eic_code = ElectricityCostsProvider.get_EIC_for_country(alpha3)
        if not security_token:
            raise APIAuthenticationError("No ENTSOE API key found!")

        periodStart = datetime.now(timezone.utc).replace(hour=0, minute=0)
        periodEnd = periodStart + timedelta(days=1)

        periodStart = periodStart.strftime("%Y%m%d%H%M")  # YYYYMMDDHHMM e.g. 202509061200
        periodEnd = periodEnd.strftime("%Y%m%d%H%M")

        url = (f"https://web-api.tp.entsoe.eu/api?documentType=A44&periodStart={periodStart}&periodEnd={periodEnd}"
               f"&out_Domain={eic_code}&in_Domain={eic_code}&securityToken={security_token}")
        r = requests.get(url)
        if r.status_code != 200:
            raise APIError("An error occurred while retrieving the price data from ENTSOE")

        return xmltodict.parse(r.content)

    @staticmethod
    def get_average_price_for_country(alpha3: str) -> float:
        """
        Get average electricity price for a country.
        
        Args:
            alpha3: ISO 3166-1 alpha-3 country code
            
        Returns:
            Average electricity price as float
            
        Raises:
            APIError: When API is unreachable
            APIResponseParsingError: When the API response cannot be parsed
            APIMissingValueError: When no price data is available for the country
        """
        result = ElectricityCostsProvider.get_price_for_country(alpha3)

        if not result:
            raise APIError(
                "Could not reach the ENTSO-E API. Please try again later or contact system administrator"
            )

        # Check for API error response
        if "Acknowledgement_MarketDocument" in result:
            try:
                error_msg = result["Acknowledgement_MarketDocument"]["Reason"]["text"]
                raise APIError(f"{error_msg} not found")
            except KeyError:
                raise APIResponseParsingError("Unexpected error response format from the API")

        # Extract and calculate average price
        try:
            timeseries = result["Publication_MarketDocument"]["TimeSeries"]

            # Normalize timeseries to dict if it's a list
            if isinstance(timeseries, list):
                if not timeseries or len(timeseries) == 0:
                    raise APIMissingValueError(
                        f"No electricity prices found for {alpha3}"
                    )
                timeseries = timeseries[0]

            values = timeseries["Period"]["Point"]
            if not values:
                raise APIMissingValueError(
                    f"No electricity prices found for {alpha3}"
                )

            prices = [float(record["price.amount"]) for record in values]
            if not prices:
                raise APIMissingValueError(
                    f"No electricity prices found for {alpha3}"
                )

            return sum(prices) / len(prices)

        except KeyError as e:
            raise APIResponseParsingError("Unexpected error response format from the API") from e
        except (ValueError, TypeError) as e:
            raise APIResponseParsingError("Error parsing price data") from e

    @staticmethod
    def _temporal_granularity_to_ttl(temporalGranularity: str) -> int:
        """
        Convert the temporal granularity string to a time-to-live (TTL) value in seconds.
        """
        temporalGranularity = temporalGranularity.lower()
        if temporalGranularity == '15_minutes':
            return 15 * 60
        elif temporalGranularity == 'hourly':
            return 60 * 60
        elif temporalGranularity == 'daily':
            return 24 * 60 * 60
        elif temporalGranularity == 'monthly':
            return 30 * 24 * 60 * 60
        elif temporalGranularity == 'quarterly':
            return 90 * 24 * 60 * 60
        elif temporalGranularity == 'yearly':
            return 365 * 24 * 60 * 60
        else:
            raise ValueError(f"Invalid temporal granularity: {temporalGranularity}")

    @staticmethod
    def get_cache_scheduler(temporalGranularity: str = 'hourly') -> CacheService:
        endpoints = []
        if temporalGranularity.lower() in ['15_minutes', 'hourly']:
            for country in ElectricityCostsProvider.get_eic_countries():
                url = f"{ElectricityMapsService.base_url}/price-day-ahead/latest?zone={country.zone_code}&temporalGranularity={temporalGranularity}"
                endpoints.append(url)
        elif temporalGranularity.lower() in ['daily', 'monthly', 'quarterly', 'yearly']:
            datetime_parameter = (datetime.now() - timedelta(seconds=ElectricityCostsProvider._temporal_granularity_to_ttl(temporalGranularity))).strftime("%Y-%m-%dT%H:%M:00Z")
            for country in ElectricityCostsProvider.get_eic_countries():
                url = f"{ElectricityMapsService.base_url}/price-day-ahead/past?zone={country.zone_code}&datetime={datetime_parameter}&temporalGranularity={temporalGranularity}"
                endpoints.append(url)
        api_token = ElectricityMapsService._get_api_key()
        cache_service = CacheService(name=f"electricity_prices_cache_{temporalGranularity}",
                                     endpoints=endpoints,
                                     ttl=ElectricityCostsProvider._temporal_granularity_to_ttl(temporalGranularity),
                                     headers={"auth-token": api_token})
        return cache_service