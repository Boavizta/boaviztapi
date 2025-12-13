from fastapi import APIRouter, status, Body, HTTPException
from typing import List

from boaviztapi.service.currency_converter import CurrencyConverter
from boaviztapi.model.currency.currency_models import Currency, CurrencyWithValue, CurrencyConversionRequest

currency_router = APIRouter(
    prefix='/v1/currency',
    tags=['currency']
)

@currency_router.get('/available_currencies',
                     response_description="Return all available currencies",
                     response_model=List[Currency],
                     status_code=status.HTTP_200_OK,
                     response_model_by_alias=False)
async def get_available_currencies():
    return CurrencyConverter.get_available_currencies()

@currency_router.post('/convert',
                     response_description="Convert a value from a source currency to a target currency",
                     response_model=CurrencyWithValue,
                     status_code=status.HTTP_200_OK,
                     response_model_by_alias=False,
                     response_model_exclude_none=True)
async def convert_currency(conversion_request: CurrencyConversionRequest = Body(...)):
    try:
        return await CurrencyConverter.convert(source_currency=conversion_request.source_currency,
                                         target_currency=conversion_request.target_currency,
                                         amount=conversion_request.amount)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

