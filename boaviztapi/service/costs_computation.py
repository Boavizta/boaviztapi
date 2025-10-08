import os
from typing import Union

import pandas as pd
from boaviztapi import config
from boaviztapi import data_dir
from boaviztapi.model.component import Component
from boaviztapi.model.device import Device

_electricity_prices_df = pd.read_csv(os.path.join(data_dir,
                                                  'electricity/european_wholesale_electricity_price_data_monthly.csv'))


def compute_electricity_costs(model: Union[Component, Device], duration=config["default_duration"]) -> dict:
    location = model.usage.usage_location.value
    if not is_valid_countrycode(location):
        return {"error": "Invalid country code!"}
    if not model.usage.avg_power.is_set():
        return {"error": "Avg power is not set!"}

    return {
        "min": compute_single_cost(model.usage.avg_power.min, duration, location),
        "avg": compute_single_cost(model.usage.avg_power.value, duration, location),
        "max": compute_single_cost(model.usage.avg_power.max, duration, location),
        "unit": "€",
        "warnings": [
            "Default energy prices were used in this calculation. The energy price default"
            " is the average yearly energy price in the given location."
        ]
    }


def is_valid_countrycode(country_code: str) -> bool:
    country_list = _electricity_prices_df["ISO3 Code"].unique()
    if country_code in country_list:
        return True
    return False


def compute_single_cost(power: float, duration: int, location: str) -> float:
    """
    Compute the electricity costs of running the device/component for the specified duration.
    The electricity costs is deduced by averaging the monthly costs over an entire year.

    @param power: The electricity power in W (Watts)
    @param duration: The duration of the electricity cost calculation in hours
    @param location: The location of the electricity cost calculation in ISO3 letter codification
    """
    # Eur / MWh
    yearly_price = _electricity_prices_df.query(f"`ISO3 Code` == '{location}'")["Price (EUR/MWhe)"].mean()
    return yearly_price * duration * (power * 10 ** -6)
