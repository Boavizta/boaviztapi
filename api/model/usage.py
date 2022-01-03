import string
from abc import abstractmethod

import pandas as pd

from typing import Optional

from pydantic import BaseModel

from api.model.components.component import Component

_electricity_emission_factors_df = pd.read_csv('./data/electricity/usage_impact_factors.csv')


class Usage(Component):
    TYPE = "USAGE"

    max_power: Optional[float] = None
    idle_power: Optional[float] = None
    yearly_electrical_consumption: Optional[float] = None
    life_duration: Optional[int] = None
    usage_location: Optional[str] = None
    idle_ratio: Optional[float] = None
    workload_ratio: Optional[float] = None

    gwp_factor: Optional[float] = None
    pe_factor: Optional[float] = None
    adp_factor: Optional[float] = None

    _DEFAULT_USAGE_LOCATION = "EU27+1"
    _DEFAULT_LIFE_DURATION = 5
    _DEFAULT_IDLE_RATIO = 0.2
    _DEFAULT_IDLE_PERCENTAGE_MAX_POWER = 0.1
    _DEFAULT_MEDIUM_LOAD_RATE = 0.5
    _DEFAULT_MAX_POWER = 100

    def impact_gwp(self) -> float:
        return self.yearly_electrical_consumption * self.life_duration * self.gwp_factor

    def impact_pe(self) -> float:
        return self.yearly_electrical_consumption * self.life_duration * self.pe_factor

    def impact_adp(self):
        return self.yearly_electrical_consumption * self.life_duration * self.adp_factor

    def smart_complete_data(self):

        if self.max_power is None:
            self.max_power = self._DEFAULT_MAX_POWER
        if self.idle_power is None:
            self.idle_power = self._DEFAULT_IDLE_PERCENTAGE_MAX_POWER * self.max_power

        if self.idle_ratio is None:
            self.idle_ratio = self._DEFAULT_IDLE_RATIO

        if self.usage_location is None:
            self.usage_location = self._DEFAULT_USAGE_LOCATION
        else:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            if len(sub) == 0:
                self.usage_location = self._DEFAULT_USAGE_LOCATION

        if self.life_duration is None:
            self.life_duration = self._DEFAULT_LIFE_DURATION
        if self.idle_ratio is None:
            self.idle_ratio = self._DEFAULT_IDLE_RATIO
        if self.workload_ratio is None:
            self.workload_ratio = self._DEFAULT_MEDIUM_LOAD_RATE

        if self.gwp_factor is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self.gwp_factor = float(sub['gwp_emission_factor'])

        if self.pe_factor is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self.pe_factor = float(sub['pe_emission_factor'])

        if self.adp_factor is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self.adp_factor = float(sub['adp_emission_factor'])

        if self.yearly_electrical_consumption is None:
            self.yearly_electrical_consumption = \
                (self.max_power*(1-self.idle_ratio)
                 + self.idle_ratio * self.idle_power) \
                * 365 * 24