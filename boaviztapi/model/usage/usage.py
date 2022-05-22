import os

import pandas as pd

from typing import Dict, Optional

from pydantic import BaseModel

from boaviztapi.model.components import data_dir
from boaviztapi.model.usage.consumption_profile import ConsumptionProfile

_electricity_emission_factors_df = pd.read_csv(os.path.join(data_dir, 'electricity/electricity_impact_factors.csv'))


class Usage(BaseModel):
    TYPE = "USAGE"
    hash: str = None

    _DEFAULT_USAGE_LOCATION = "EEE"
    _DEFAULT_YEAR_USE_TIME = 1
    _DEFAULT_TIME_PER_WORKLOAD = {"100": (3.6 / 24),
                                  "50": (13.2 / 24),
                                  "10": (4.8 / 24),
                                  "0": (2.4 / 24)}

    years_use_time: Optional[float] = None
    days_use_time: Optional[float] = None
    hours_use_time: Optional[float] = None

    hours_electrical_consumption: Optional[float] = None
    time_per_workload: Optional[Dict[str, float]] = None
    consumption_profile: ConsumptionProfile = None

    usage_location: Optional[str] = None
    gwp_factor: Optional[float] = None
    pe_factor: Optional[float] = None
    adp_factor: Optional[float] = None

    def get_gwp_factor(self):
        if not self.gwp_factor:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.get_usage_location()]
            self.gwp_factor = float(sub['gwp_emission_factor'])
        return self.gwp_factor

    def get_adp_factor(self):
        if not self.adp_factor:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self.adp_factor = float(sub['adpe_emission_factor'])
        return self.gwp_factor

    def get_pe_factor(self):
        if not self.pe_factor:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self.pe_factor = float(sub['pe_emission_factor'])
        return self.gwp_factor

    def get_usage_location(self):
        if not self.usage_location:
            self.usage_location = self._DEFAULT_USAGE_LOCATION
        else:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            if len(sub) == 0:
                self.usage_location = self._DEFAULT_USAGE_LOCATION
        return self.usage_location

    def get_years_use_time(self):
        if not self.years_use_time:
            if self.get_hours_use_time() == 0 and self.get_days_use_time() == 0:
                self.years_use_time = self._DEFAULT_YEAR_USE_TIME
        return self.years_use_time

    def get_hours_use_time(self):
        if not self.hours_use_time:
            self.hours_use_time = 0
        return self.hours_use_time

    def get_days_use_time(self):
        if not self.days_use_time:
            self.hours_use_time = 0
        return self.hours_use_time

    def get_hours_electrical_consumption(self):
        if not self.hours_electrical_consumption:
            if self.get_time_per_workload():
                self.get_consumption_profile()
                pass  # Apply consumption profile 2 time_per_workload
            else:
                self.hours_electrical_consumption = 0
        return self.hours_electrical_consumption

    def get_time_per_workload(self):
        if not self.time_per_workload:
            self.time_per_workload = self._DEFAULT_TIME_PER_WORKLOAD
        return self.time_per_workload

    def get_duration_hours(self) -> float:
        return (self.get_hours_use_time() or 0) + \
               ((self.get_days_use_time() or 0) * 24) + \
               ((self.get_years_use_time() or 0) * 365 * 24)

    def get_consumption_profile(self, model):
        return None

    def __hash__(self) -> int:
        # TODO: TO ENHANCE
        return 0


class UsageServer(Usage):
    _DEFAULT_OTHER_CONSUMPTION_RATIO = 0.33

    other_consumption_ratio: Optional[float] = None

    def get_other_consumption_ratio(self):
        if not self.other_consumption_ratio:
            self.other_consumption_ratio = self._DEFAULT_OTHER_CONSUMPTION_RATIO
        return self.other_consumption_ratio

    def get_consumption_profile(self, model):
        if not self.consumption_profile:
            pass  # TODO
        return self.consumption_profile


class UsageCloud(UsageServer):
    _DEFAULT_INSTANCE_PER_SERVER = 1

    instance_per_server: Optional[float] = None

    def get_instance_per_server(self):
        if not self.instance_per_server:
            self.instance_per_server = self._DEFAULT_INSTANCE_PER_SERVER
        return self.instance_per_server

    def get_consumption_profile(self, model):
        if not self.consumption_profile:
            pass  # TODO from archetype
        return self.consumption_profile


class UsageCPU(Usage):
    def get_consumption_profile(self, model):
        if not self.consumption_profile:
            pass  # TODO from cpu model
        return self.consumption_profile
