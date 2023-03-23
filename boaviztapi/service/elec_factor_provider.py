import os
from datetime import datetime, timedelta

import pandas as pd
import requests

from boaviztapi import data_dir

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


if __name__ == '__main__':
    elec_provider = ElectricityMap()
