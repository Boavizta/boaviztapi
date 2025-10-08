import logging
import os
from datetime import datetime, timezone, timedelta

import pandas as pd
import requests
import xmltodict

from boaviztapi import data_dir
from boaviztapi.application_context import get_app_context

_logger = logging.getLogger(__name__)

df = pd.read_csv(os.path.join(data_dir, 'electricity/eic_codes.csv'))


def get_eic_countries() -> list[dict]:
    """
    Get the list of EIC codes and their countries and return it as a dict
    """
    return df.to_dict(orient='records')


def get_EIC_for_country(iso3_country: str) -> str:
    return df.query(f"`ISO3 Code` == '{iso3_country}' ")["EIC_code"].iloc[0]


def get_price_for_country(iso3_country: str) -> dict | None:
    ctx = get_app_context()
    security_token = ctx.entsoe_api_key
    eic_code = get_EIC_for_country(iso3_country)
    if not security_token:
        _logger.warning("No security token was found for ENTSOE_API")
        return None

    periodStart = datetime.now(timezone.utc).replace(hour=0, minute=0)
    periodEnd = periodStart + timedelta(days=1)

    periodStart = periodStart.strftime("%Y%m%d%H%M")  # YYYYMMDDHHMM e.g. 202509061200
    periodEnd = periodEnd.strftime("%Y%m%d%H%M")

    url = f"https://web-api.tp.entsoe.eu/api?documentType=A44&periodStart={periodStart}&periodEnd={periodEnd}&out_Domain={eic_code}&in_Domain={eic_code}&securityToken={security_token}"
    r = requests.get(url)
    if r.status_code == 200:
        return xmltodict.parse(r.content)
    _logger.error("get_price_for_country returned status code %s", r.status_code)
    return None
