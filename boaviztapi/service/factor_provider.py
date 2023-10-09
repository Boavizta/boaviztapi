import os
from pathlib import Path

import pandas as pd
import yaml
from boaviztapi import data_dir

config_file = os.path.join(data_dir, 'factors.yml')
impact_factors = yaml.safe_load(Path(config_file).read_text())


def get_impact_factor(item, impact_type) -> dict:
    if impact_factors.get(item):
        if impact_factors.get(item).get(impact_type):
            return impact_factors.get(item).get(impact_type)
    raise NotImplementedError


def get_electrical_impact_factor(usage_location, impact_type) -> dict:
    if impact_factors["electricity"].get(usage_location):
        if impact_factors["electricity"].get(usage_location).get(impact_type):
            return impact_factors["electricity"].get(usage_location).get(impact_type)
    raise NotImplementedError


def get_electrical_min_max(impact_type, type) -> float:
    if impact_factors["electricity"].get("min-max").get(impact_type):
        if impact_factors["electricity"].get("min-max").get(impact_type).get(type):
            return impact_factors["electricity"].get("min-max").get(impact_type).get(type)
    raise NotImplementedError


def get_available_countries(reverse=False):
    if reverse:
        return {v: k for k, v in impact_factors["electricity"]["available_countries"].items()}
    return impact_factors["electricity"]["available_countries"]


def get_available_iot_functional_block():
    if impact_factors.get("IoT"):
        return impact_factors.get("IoT").keys()


def get_available_iot_hsl():
    response = {}
    for functional_block in get_available_iot_functional_block():
        response[functional_block] = impact_factors.get("IoT").get(functional_block).keys()
    return response


def get_iot_impact_factor(functional_block, hsl, impact_type):
    if impact_factors["IoT"].get(functional_block):
        if impact_factors["IoT"].get(functional_block).get(hsl):
            if impact_factors["IoT"].get(functional_block).get(hsl)["manufacture"].get(impact_type) is not None and impact_factors["IoT"].get(functional_block).get(hsl)["eol"].get(impact_type) is not None:
                return (impact_factors["IoT"].get(functional_block).get(hsl)["manufacture"][impact_type]
                        + impact_factors["IoT"].get(functional_block).get(hsl)["eol"][impact_type])
    raise NotImplementedError


"""
_electricity_emission_factors_df = pd.read_csv(
    os.path.join(data_dir, 'electricity/electricity_impact_factors.csv'))
class ElecFactorProvider:
    def get(self, criteria, location, date):
        pass
    def get_range(self, criteria, location, date1, date2):
        pass
class BoaviztaFactors(ElecFactorProvider):
    def get(self, criteria, usage_location, date=None):
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == usage_location]
        return float(sub[f"{criteria}_emission_factor"]), sub[f"{criteria}_emission_source"].iloc[0], 0, ["The impact factor is averaged over the year"]
    def get_range(self, criteria, usage_location, date1=None, date2=None):
        return self.get(criteria,usage_location)

class ElectricityMap(ElecFactorProvider):
    auth_token = "6QGqlsF7ZcdUN6TMB7jX9DMsYKeGHbVl"
    url = "https://api-access.electricitymaps.com/2w97h07rvxvuaa1g"
    now = datetime.now()
    def get(self, criteria, location, date):
        zone = self._location_to_em_zone(location)
        if self.now - timedelta(hours=1) < date < self.now + timedelta(hours=1):
            return self._get_current(zone)
        elif date < self.now:
            return self._get_history(zone, date)
        else:
            return NotImplementedError
    def get_range(self, criteria, zone, date1, date2):
        pass
    def _get_current(self, zone):
        reponse = requests.get(f"{self.url}/carbon-intensity/latest?zone={zone}",
                headers={"X-BLOBR-KEY": self.auth_token}).json()

        return reponse["carbonIntensity"]/1000, f"electricity map response : {reponse}", 0, []
    def _get_history(self, zone, date):
        reponse = requests.get(f"{self.url}/carbon-intensity/history?zone={zone}&datetime={date}",
                               headers={"X-BLOBR-KEY": self.auth_token }).json()

        return reponse
    def _location_to_em_zone(self, location):
        return location
"""
