from typing import Optional

from pydantic import BaseModel, Field


class Currency(BaseModel):
    symbol: str = Field(..., description="ISO 4217 currency code")
    name: Optional[str] = Field(..., description="Currency name")

class CurrencyWithValue(Currency):
    value: float = Field(
        ..., description="Value of the currency in the current locale"
    )

class CurrencyConversionRequest(BaseModel):
    source_currency: str = Field(..., description="Source currency")
    target_currency: str = Field(..., description="Target currency")
    amount: float = Field(..., description="Amount to convert")
