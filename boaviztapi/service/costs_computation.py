import os
from typing import Union, Any

import pandas as pd
from boaviztapi import config
from boaviztapi import data_dir
from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
from boaviztapi.service.costs_provider import ElectricityCostsProvider

_electricity_prices_df = pd.read_csv(os.path.join(data_dir,
                                                  'electricity/european_wholesale_electricity_price_data_monthly.csv'))


def compute_electricity_costs(model: Union[Component, Device], duration=config["default_duration"], location: str = None) -> dict:
    if not location:
        location = model.usage.usage_location.value
    if not is_valid_zone_code(location):
        return {"error": f"Invalid zone code '{location}'!"}
    if not model.usage.avg_power.is_set():
        return {"error": "Avg power is not set!"}

    return {
        "min": compute_single_cost(model.usage.avg_power.min, duration, location),
        "avg": compute_single_cost(model.usage.avg_power.value, duration, location),
        "max": compute_single_cost(model.usage.avg_power.max, duration, location),
        "warnings": [
            "Default energy prices were used in this calculation. The energy price default"
            " is the average yearly energy price in the given location."
        ]
    }


def is_valid_iso3country(country_code: str) -> bool:
    country_list = ElectricityCostsProvider.get_eic_countries()
    if country_code in [item.alpha_3 for item in country_list]:
        return True
    return False

def is_valid_zone_code(zone_code: str) -> bool:
    country_list = ElectricityCostsProvider.get_eic_countries()
    if zone_code in [item.zone_code for item in country_list]:
        return True
    return False


def compute_single_cost(power: float, duration: int, location: str) -> dict[str, str]:
    """
    Compute the electricity costs of running the device/component for the specified duration.
    The electricity costs are deduced by averaging the monthly costs over an entire year.

    @param power: The electricity power in W (Watts)
    @param duration: The duration of the electricity cost calculation in hours
    @param location: The location of the electricity cost calculation in ISO3 letter codification
    """
    # Eur / MWh
    realtime_price = ElectricityCostsProvider.get_price_for_country_elecmaps(location)
    if realtime_price and realtime_price['value'] and realtime_price['unit']:
        yearly_price = realtime_price['value'] * duration * (power * 10 ** -6)
        return {
            "price": yearly_price,
            "unit": realtime_price['unit']
        }
    country_list = ElectricityCostsProvider.get_eic_countries()
    country_alpha3 = None
    for item in country_list:
        if item.alpha_3 == location:
            country_alpha3 = item.alpha_3
    if not country_alpha3:
        raise ValueError(f"Invalid zone code: {location}")
    yearly_price = _electricity_prices_df.query(f"`ISO3 Code` == '{country_alpha3}'")["Price (EUR/MWhe)"].mean()
    return {
        "price": yearly_price * duration * (power * 10 ** -6),
        "unit": "EUR/MWh"
    }
