from abc import abstractmethod

import pandas as pd

from typing import Optional

from api.model.components.component import Component

_electricity_emission_factors_df = pd.read_csv('./data/electricity/usage_impact_factors.csv')


class Usage(Component):
    TYPE = "USAGE"

    yearly_electrical_consumption: Optional[float] = None
    year_use_time: Optional[int] = None
    usage_location: Optional[str] = None

    gwp_factor: Optional[float] = None
    pe_factor: Optional[float] = None
    adp_factor: Optional[float] = None

    _DEFAULT_USAGE_LOCATION = "EU27+1"
    _DEFAULT_YEAR_USE_TIME = 1

    @abstractmethod
    def impact_gwp(self) -> float:
        return self.yearly_electrical_consumption * self.year_use_time * self.gwp_factor

    @abstractmethod
    def impact_pe(self) -> float:
        return self.yearly_electrical_consumption * self.year_use_time * self.pe_factor

    @abstractmethod
    def impact_adp(self):
        return self.yearly_electrical_consumption * self.year_use_time * self.adp_factor

    @abstractmethod
    def get_electrical_consumption(self):
        pass

    @abstractmethod
    def smart_complete_data(self):

        if self.usage_location is None:
            self.usage_location = self._DEFAULT_USAGE_LOCATION
        else:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            if len(sub) == 0:
                self.usage_location = self._DEFAULT_USAGE_LOCATION

        if self.year_use_time is None:
            self.year_use_time = self._DEFAULT_YEAR_USE_TIME

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
            self.yearly_electrical_consumption = self.get_electrical_consumption()


class UsageServer(Usage):
    # TODO: Set default workload ratio and corresponding power of DELL R740 LCA

    def impact_gwp(self) -> float:
        return super().impact_gwp()

    def impact_pe(self) -> float:
        return super().impact_pe()

    def impact_adp(self):
        return super().impact_adp()

    def get_electrical_consumption(self):
        # TODO : Apply server usage formula according to #21
        pass

    def smart_complete_data(self):
        # TODO : Set default value of workload ratio and corresponding power if not set
        super().smart_complete_data()


class UsageCloud(Usage):

    def impact_gwp(self) -> float:
        return super().impact_gwp()

    def impact_pe(self) -> float:
        return super().impact_pe()

    def impact_adp(self):
        return super().impact_adp()

    def get_electrical_consumption(self):
        # TODO : Apply cloud formula according to #29
        pass

    def smart_complete_data(self):
        super().smart_complete_data()
