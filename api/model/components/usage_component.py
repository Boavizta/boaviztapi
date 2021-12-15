import string
from abc import abstractmethod

import pandas as pd

from api.model.components.component import Component
from typing import Optional

_electricity_emission_factors_df = pd.read_csv('./api/model/components/carbon-intensity-electricity.csv')


class UsageComponent(Component):
    power_supply: Optional[float] = None
    yearly_electrical_consumption: Optional[float] = None
    life_duration: Optional[int] = None
    usage_location: Optional[string] = None
    idle_percentage: Optional[float] = None
    medium_load_rate: Optional[float] = None
    carbon_intensity: Optional[float] = None
    primary_emission_factor: Optional[float] = None

    _DEFAULT_USAGE_LOCATION = "EU27+1"
    _DEFAULT_LIFE_DURATION = 5
    _DEFAULT_IDLE_PERCENTAGE = 10.0
    _DEFAULT_MEDIUM_LOAD_RATE = 100.0

    @abstractmethod
    def impact_gwp(self) -> float:
        return self.yearly_electrical_consumption * self.life_duration * self.carbon_intensity

    @abstractmethod
    def impact_pe(self) -> float:
        raise self.yearly_electrical_consumption * self.life_duration * self.carbon_intensity

    @abstractmethod
    def impact_adp(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def smart_complete_data(self):

        if self.usage_location is None:
            self.usage_location = self._DEFAULT_USAGE_LOCATION
        else:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            if len(sub) == 0:
                self.usage_location = self._DEFAULT_USAGE_LOCATION

        if self.life_duration is None:
            self.life_duration = self._DEFAULT_LIFE_DURATION
        if self.idle_percentage is None:
            self.idle_percentage = self._DEFAULT_IDLE_PERCENTAGE
        if self.medium_load_rate is None:
            self.medium_load_rate = self._DEFAULT_MEDIUM_LOAD_RATE

        if self.carbon_intensity is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            sub = sub[sub['year'] == "2020"]
            self.carbon_intensity = float(sub['carbon_intensity'])

        if self.primary_emission_factor is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            sub = sub[sub['year'] == "2020"]
            self.primary_emission_factor = float(sub['primary_emission_factor'])

        if self.yearly_electrical_consumption is None:
            if self.power_supply is None:
                self.power_supply = 0  # TODO
            self.yearly_electrical_consumption = self.power_supply * self.medium_load_rate * \
                                                 self.idle_percentage * 365 * 24
