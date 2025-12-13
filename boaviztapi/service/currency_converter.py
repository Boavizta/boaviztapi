import os
from typing import Any, Dict, List

from boaviztapi import data_dir
from boaviztapi.model.currency.currency_models import Currency, CurrencyWithValue
from boaviztapi.service.cache.cache import CacheService
from fastapi_cache.decorator import cache
import pandas as pd

url = "https://api.frankfurter.dev/v1/latest"

currencies_df = pd.read_csv(os.path.join(data_dir, 'currency/frankfurter_currencies.csv'))

class CurrencyConverter:
    @staticmethod
    async def get_cache_scheduler() -> CacheService:
        endpoints = []
        currencies: List[Currency] = CurrencyConverter.get_available_currencies()
        for currency in currencies:
            endpoints.append(CurrencyConverter._url_for_currency(currency.symbol))
        return CacheService(name="currency_converter_cache", endpoints=endpoints, ttl=3600 * 24)

    @staticmethod
    @cache(expire=3600 * 24)
    async def _get_currency_table(base_currency: str = "EUR") -> Dict[str, Any]:
        """
        Get the conversion rates for all currencies given a base currency.

        Args:
            base_currency: The base currency to use for the conversion rates. Defaults to EUR.

        Returns:
            Dictionary containing the conversion rates for each currency.
        """
        CurrencyConverter.validate_currency(base_currency)
        _cache = await CurrencyConverter.get_cache_scheduler()
        _cached_results = await _cache.get_results()
        return _cached_results[CurrencyConverter._url_for_currency(base_currency)]["rates"]

    @staticmethod
    def get_available_currencies() -> List[Currency]:
        """
        Get a list of all available currencies and their symbols.
        """
        currencies = []
        for item in currencies_df.to_dict(orient='records'):
            currencies.append(Currency(symbol=item['Symbol'], name=item['Name']))
        return currencies

    @staticmethod
    def get_currency_by_symbol(symbol: str) -> Currency | None:
        """
        Fetches a currency object based on the provided symbol.

        Args:
            symbol: A string representing the currency symbol to search for.

        Returns:
            Currency: The corresponding Currency object that matches the given symbol.

        Raises:
            ValueError : If no currency is found matching the provided symbol.
        """
        _currencies = CurrencyConverter.get_available_currencies()
        CurrencyConverter.validate_currency(symbol)
        for cur in _currencies:
            if cur.symbol == symbol:
                return cur
        return None

    @staticmethod
    async def convert(source_currency: str, target_currency: str, amount: float) -> CurrencyWithValue | None:
        """
        Converts an amount of a source currency to a target currency.

        Args:
            source_currency: The currency to convert from in ISO 4217 format.
            target_currency: The currency to convert to in ISO 4217 format.
            amount: The amount to convert.

        Returns:
            Amount in target currency.
        """
        if source_currency is None or target_currency is None or amount is None:
            return None
        if source_currency == target_currency:
            return CurrencyWithValue(symbol=source_currency, value=amount, name=None)

        CurrencyConverter.validate_currency(source_currency)
        CurrencyConverter.validate_currency(target_currency)

        table = await CurrencyConverter._get_currency_table(base_currency=source_currency)
        return CurrencyWithValue(symbol=target_currency, value=amount * table[target_currency], name=None)

    @staticmethod
    def _url_for_currency(currency: str) -> str:
        return f"{url}?base={currency}"

    @staticmethod
    def validate_currency(c: str) -> str:
        currencies: List[Currency] = CurrencyConverter.get_available_currencies()
        currency_symbols = [currency.symbol for currency in currencies]
        if c not in [currency.symbol for currency in currencies]:
            raise ValueError(f"Invalid or unsupported source currency: '{c}'. The supported values are: {currency_symbols}")
        return c
