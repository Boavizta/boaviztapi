import os
from abc import abstractmethod

import pandas as pd

from typing import Dict, Optional

from boaviztapi.model.components import data_dir
from boaviztapi.model.components.component import Component

_electricity_emission_factors_df = pd.read_csv(os.path.join(data_dir, 'electricity/usage_impact_factors.csv'))


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
    def get_yearly_electrical_consumption(self):
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

    def __hash__(self) -> int:
        # TODO: TO ENHANCE
        return 0


class UsageServer(Usage):
    # TODO: Set default workload ratio and corresponding power of DELL R740 LCA
    _DEFAULT_MAX_POWER = 510

    _DEFAULT_WORKLOAD = {"100": {"time": (3.6/24), "power": 1.0},
                         "50": {"time": (13.2/24), "power": 369/510},
                         "10": {"time": (4.8/24), "power": 261/510},
                         "idle": {"time": (2.4/24), "power": 201/510},
                         "off": {"time": 0., "power": 0.}
                         }

    max_power: Optional[float] = None
    workload: Optional[Dict[str, Dict[str, float]]] = None

    def impact_gwp(self) -> float:
        return super().impact_gwp()

    def impact_pe(self) -> float:
        return super().impact_pe()

    def impact_adp(self):
        return super().impact_adp()

    def get_yearly_electrical_consumption(self) -> float:
        year_electrical_consumption = 0
        for values in self.workload.values():
            year_electrical_consumption += values["time"] * 24 * 365 * values["power"] * self.max_power
        return year_electrical_consumption / 1000

    def smart_complete_data(self):
        # TODO : Set default value of workload ratio and corresponding power if not set
        super().smart_complete_data()
        if self.yearly_electrical_consumption is None:
            if self.max_power is None:
                self.max_power = self._DEFAULT_MAX_POWER
            if self.workload is None:
                self.workload = self._DEFAULT_WORKLOAD

            self.yearly_electrical_consumption = self.get_yearly_electrical_consumption()


class UsageCloud(Usage):

    def impact_gwp(self) -> float:
        return super().impact_gwp()

    def impact_pe(self) -> float:
        return super().impact_pe()

    def impact_adp(self):
        return super().impact_adp()

    def get_yearly_electrical_consumption(self):
        # TODO : Apply cloud formula according to #29
        pass

    def smart_complete_data(self):
        super().smart_complete_data()
