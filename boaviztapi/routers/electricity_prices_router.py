from typing import Annotated

from fastapi import APIRouter, Query, HTTPException
from fastapi_cache.decorator import cache

from boaviztapi import factors
from boaviztapi.routers.openapi_doc.descriptions import electricity_available_countries, electricity_price
from boaviztapi.service.costs_provider import get_eic_countries, get_price_for_country

electricity_prices_router = APIRouter(
    prefix='/v1/electricity',
    tags=['electricity'],
)


@cache(expire=60 * 60 * 24)
@electricity_prices_router.get('/available_countries', description=electricity_available_countries)
async def get_available_countries():
    return get_eic_countries()


@electricity_prices_router.get('/price', description=electricity_price)
@cache(expire=3600)
async def get_electricity_price(
        iso3_country: Annotated[str | None, Query(example=factors["electricity"]["entsoe_supported_countries"])] = None):
    if iso3_country is None:
        raise HTTPException(status_code=400, detail="iso3_country cannot be empty!")
    if iso3_country not in [c["ISO3 Code"] for c in get_eic_countries()]:
        raise HTTPException(status_code=400, detail="iso3_country is not valid!")

    result = get_price_for_country(iso3_country)
    if not result:
        raise HTTPException(status_code=404, detail=f"Could not reach the pricing API. Please try again later or"
                                                    f" contact system administrator")
    if "Acknowledgement_MarketDocument" in result:
        # error case
        error_msg = result["Acknowledgement_MarketDocument"]["Reason"]["text"]
        raise HTTPException(status_code=404, detail=f"{error_msg} not found")
    timeseries = result["Publication_MarketDocument"]["TimeSeries"]
    if len(timeseries) > 1:
        timeseries = timeseries[0]
    values = timeseries["Period"]["Point"]
    avg_price = ([float(record["price.amount"]) for record in values])
    return sum(avg_price) / len(avg_price)
