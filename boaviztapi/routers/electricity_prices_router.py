from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache
from pydantic import AfterValidator

from boaviztapi.dto.electricity.electricity import Country
from boaviztapi.routers.openapi_doc.descriptions import electricity_available_countries, electricity_price, \
    carbon_intensity, power_breakdown, electricity_prices_cache
from boaviztapi.routers.openapi_doc.examples import electricity_carbon_intensity, electricity_power_breakdown, \
    electricity_maps_price
from boaviztapi.service.carbon_intensity_provider import CarbonIntensityProvider
from boaviztapi.service.costs_provider import ElectricityCostsProvider
from boaviztapi.service.exceptions import APIMissingValueError, APIError, APIAuthenticationError
from boaviztapi.utils.validators import check_zone_code_in_electricity_maps

electricity_prices_router = APIRouter(
    prefix='/v1/electricity',
    tags=['electricity'],
)


@electricity_prices_router.get('/available_countries', description=electricity_available_countries,
                               response_model=list[Country])
@cache(expire=60 * 60 * 24)  # 1 day
async def get_available_countries():
    return ElectricityCostsProvider.get_eic_countries()


@electricity_prices_router.get('/price', description=electricity_price,
                               response_model=Country,
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
        temporalGranularity: str = Query(examples=["5_minutes", "15_minutes", "hourly"], default="hourly")):
    try:
        return ElectricityCostsProvider.get_price_for_country_elecmaps(zone, temporalGranularity)
    except APIMissingValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@electricity_prices_router.get('/prices', description=electricity_prices_cache,
                               responses={200: {
                                   "description": "Successful Response",
                                   "content": {"application/json": {"example": {"https://api.electricitymaps.com/v3/price-day-ahead/latest?zone=AT&temporalGranularity=hourly": {"zone": "AT", "datetime": "2025-11-19T20:00:00.000Z", "createdAt": "2025-11-18T12:21:16.175Z", "updatedAt": "2025-11-18T12:21:16.175Z", "value": 124.81, "unit": "EUR/MWh", "source": "nordpool.com", "temporalGranularity": "hourly"}}}}
                               }})
async def get_electricity_prices():
    return await ElectricityCostsProvider.get_cache_scheduler().get_results()


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

