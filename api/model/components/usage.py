from abc import abstractmethod

import pandas as pd

from typing import Optional

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
    _DEFAULT_LIFE_DURATION = None
    _DEFAULT_IDLE_RATIO = None
    _DEFAULT_IDLE_PERCENTAGE_MAX_POWER = None
    _DEFAULT_MEDIUM_WORKLOAD = None
    _DEFAULT_MAX_POWER = None

    @abstractmethod
    def impact_gwp(self) -> float:
        return self.yearly_electrical_consumption * self.life_duration * self.gwp_factor

    @abstractmethod
    def impact_pe(self) -> float:
        return self.yearly_electrical_consumption * self.life_duration * self.pe_factor

    @abstractmethod
    def impact_adp(self):
        return self.yearly_electrical_consumption * self.life_duration * self.adp_factor

    @abstractmethod
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
            self.workload_ratio = self._DEFAULT_MEDIUM_WORKLOAD

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


class UsageServer(Usage):
    _DEFAULT_LIFE_DURATION = 5
    _DEFAULT_IDLE_RATIO = 10 / 100  # DELL R740 ratio
    _DEFAULT_IDLE_PERCENTAGE_MAX_POWER = 40 / 100  # DELL R740 ratio
    _DEFAULT_MEDIUM_WORKLOAD = 50 / 100  # DELL R740 ratio
    _DEFAULT_MAX_POWER = 510  # DELL R740 ratio in Watt

    def impact_gwp(self) -> float:
        return super().impact_gwp()

    def impact_pe(self) -> float:
        return super().impact_pe()

    def impact_adp(self):
        return super().impact_adp()

    def smart_complete_data(self):
        super().smart_complete_data()

        if self.yearly_electrical_consumption is None:
            self.yearly_electrical_consumption = round((((self.max_power * (1 - self.idle_ratio) * self.workload_ratio) +
                                                   (self.idle_ratio * self.idle_power)) / 1000) * 365 * 24, 0)
