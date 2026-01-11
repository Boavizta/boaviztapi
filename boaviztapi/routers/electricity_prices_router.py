from copy import deepcopy
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache
from pydantic import AfterValidator

from boaviztapi.dto.electricity.electricity import Country
from boaviztapi.routers.openapi_doc.descriptions import electricity_available_countries, electricity_price, \
    carbon_intensity, power_breakdown, electricity_prices_cache, power_breakdowns_cache, carbon_free_energy_cache, \
    renewable_energy_cache
from boaviztapi.routers.openapi_doc.examples import electricity_carbon_intensity, electricity_power_breakdown, \
    electricity_maps_price
from boaviztapi.service.currency_converter import CurrencyConverter
from boaviztapi.service.electricity_maps.carbon_free_energy_provider import CarbonFreeEnergyProvider
from boaviztapi.service.electricity_maps.carbon_intensity_provider import CarbonIntensityProvider
from boaviztapi.service.electricity_maps.costs_provider import ElectricityCostsProvider
from boaviztapi.service.electricity_maps.renewable_energy_provider import RenewableEnergyProvider
from boaviztapi.service.exceptions import APIMissingValueError, APIError, APIAuthenticationError
from boaviztapi.utils.validators import check_zone_code_in_electricity_maps

electricity_prices_router = APIRouter(
    prefix='/v1/electricity',
    tags=['electricity'],
)


def validate_temporal_granularity(temporal_granularity: str) -> str:
    if temporal_granularity not in ["15_minutes", "hourly", "daily", "monthly", "quarterly", "yearly"]:
        raise ValueError(
            "Temporal granularity must be one of '15_minutes', 'hourly', 'daily', 'monthly', 'quarterly' or 'yearly'")
    return temporal_granularity


@electricity_prices_router.get('/available_countries', description=electricity_available_countries,
                               response_model=list[Country])
@cache(expire=60 * 60 * 24)  # 1 day
async def get_available_countries():
    return ElectricityCostsProvider.get_eic_countries()


@electricity_prices_router.get('/price', description=electricity_price,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": electricity_maps_price}}
                               }})
@cache(expire=3600)
async def get_electricity_price(
        zone: Annotated[str, Query(
            description="Zone code as defined in the ElectricityMaps API",
            examples=["AT"]
        ), AfterValidator(check_zone_code_in_electricity_maps)],
        temporalGranularity: str = Query(examples=["hourly"], default="hourly")):
    try:
        return await ElectricityCostsProvider.get_price_for_country_elecmaps(zone, temporalGranularity)
    except APIMissingValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@electricity_prices_router.get('/prices', description=electricity_prices_cache,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": {
                                       "https://api.electricitymaps.com/v3/price-day-ahead/latest?zone=AT&temporalGranularity=hourly": {
                                           "zone": "AT", "datetime": "2025-11-19T20:00:00.000Z",
                                           "createdAt": "2025-11-18T12:21:16.175Z",
                                           "updatedAt": "2025-11-18T12:21:16.175Z", "value": 124.81, "unit": "EUR/MWh",
                                           "source": "nordpool.com", "temporalGranularity": "hourly"}}}}
                               }})
async def get_electricity_prices(
        currency: Annotated[str | None, AfterValidator(CurrencyConverter.validate_currency)] = None,
        temporal_granularity: Annotated[
            str,
            Query(
                examples=["15_minutes", "hourly", "daily", "monthly", "quarterly", "yearly"]
            ),
            AfterValidator(validate_temporal_granularity)
        ] = 'hourly'):
    results = await ElectricityCostsProvider.get_cache_scheduler(temporal_granularity).get_results()
    if currency is None:
        return results
    results = deepcopy(results)
    for url in results:
        source_currency = str(results[url]["unit"]).split('/')[0]
        source_electricity_unit = str(results[url]["unit"]).split('/')[1]
        source_amt = results[url]["value"]
        try:
            target_amt = await CurrencyConverter.convert(source_currency, currency, source_amt)
            results[url]["value"] = target_amt.value
            results[url]["unit"] = f"{target_amt.symbol}/{source_electricity_unit}"
        except ValueError:
            results[url]["warning"] = "Could not convert this price to the requested currency!"
        except AttributeError:
            results[url]["warning"] = "Could not find a value or a unit for this price!"
    return results


@electricity_prices_router.get('/carbon_intensity', description=carbon_intensity,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": electricity_carbon_intensity}}
                               }})
@cache(expire=3600)
async def get_carbon_intensity(
        zone: Annotated[str, Query(
            description="Zone code as defined in the ElectricityMaps API",
            examples=["AT"]
        ), AfterValidator(check_zone_code_in_electricity_maps)],
        temporalGranularity: str = Query(examples=["5_minutes", "15_minutes", "hourly"], default="hourly")):
    try:
        return CarbonIntensityProvider.get_carbon_intensity(zone, temporalGranularity)
    except APIAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@electricity_prices_router.get('/power_breakdown', description=power_breakdown,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": electricity_power_breakdown}}
                               }})
@cache(expire=3600)
async def get_power_breakdown(
        zone: Annotated[str, Query(
            description="Zone code as defined in the ElectricityMaps API",
            examples=["AT"]
        ), AfterValidator(check_zone_code_in_electricity_maps)],
        temporalGranularity: str = Query(examples=["5_minutes", "15_minutes", "hourly"], default="hourly")):
    try:
        return CarbonIntensityProvider.get_power_breakdown(zone, temporalGranularity)
    except APIAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@electricity_prices_router.get('/carbon-intensities', description=power_breakdowns_cache,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": {
                                       "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=AE&temporalGranularity=hourly": {
                                           "zone": "AE",
                                           "carbonIntensity": "359",
                                           "datetime": "2026-01-11T19:00:00.000Z",
                                           "updatedAt": "2026-01-11T19:24:37.878Z",
                                           "createdAt": "2026-01-11T13:24:49.595Z",
                                           "emissionFactorType": "lifecycle",
                                           "isEstimated": True,
                                           "estimationMethod": "GENERAL_PURPOSE_ZONE_MODEL",
                                           "temporalGranularity": "hourly"}}}}}

                               })
async def get_electricity_prices():
    return await CarbonIntensityProvider.get_cache_scheduler().get_results()


@electricity_prices_router.get('/carbon-free-energy', description=carbon_free_energy_cache,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": {
                                       "https://api.electricitymaps.com/v3/carbon-free-energy/latest?zone=DE&temporalGranularity=hourly": {
                                           "zone": "DE",
                                           "datetime": "2018-04-25T18:07:00.350Z",
                                           "updatedAt": "2018-04-25T18:07:01.000Z",
                                           "createdAt": "2018-04-22T18:07:01.000Z",
                                           "unit": "%",
                                           "value": "91",
                                           "isEstimated": True,
                                           "estimationMethod": "FORECASTS_HIERARCHY",
                                           "temporalGranularity": "hourly"
                                       }}}}}})
async def get_carbon_free_energy(temporal_granularity: Annotated[
    str,
    Query(
        examples=["15_minutes", "hourly", "daily", "monthly", "quarterly", "yearly"]
    ),
    AfterValidator(validate_temporal_granularity)
] = 'hourly'):
    return await CarbonFreeEnergyProvider.get_cache_scheduler(temporal_granularity).get_results()


@electricity_prices_router.get('/renewable-energy', description=renewable_energy_cache,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": {
                                       "https://api.electricitymaps.com/v3/renewable-energy/latest?zone=DE&temporalGranularity=hourly": {
                                           "zone": "DE",
                                           "datetime": "2018-04-25T18:07:00.350Z",
                                           "updatedAt": "2018-04-25T18:07:01.000Z",
                                           "createdAt": "2018-04-22T18:07:01.000Z",
                                           "unit": "%",
                                           "value": "89",
                                           "isEstimated": True,
                                           "estimationMethod": "FORECASTS_HIERARCHY",
                                           "temporalGranularity": "hourly"
                                       }}}}}})
async def get_renewable_energy(temporal_granularity: Annotated[
    str,
    Query(
        examples=["15_minutes", "hourly", "daily", "monthly", "quarterly", "yearly"]
    ),
    AfterValidator(validate_temporal_granularity)
] = 'hourly'):
    return await RenewableEnergyProvider.get_cache_scheduler(temporal_granularity).get_results()
