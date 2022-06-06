import pandas as pd

from typing import Dict, Union

from boaviztapi.dto.usage import Usage


_electricity_emission_factors_df = pd.read_csv('./boaviztapi/data/electricity/electricity_impact_factors.csv')

_cpu_profile_file = './boaviztapi/data/consumption_profile/cpu/cpu_profile.csv'
_cloud_profile_file = './boaviztapi/data/consumption_profile/cloud/cpu_profile.csv'
_server_profile_file = './boaviztapi/data/consumption_profile/server/server_profile.csv'


class ModelUsage:
    DEFAULT_USAGE_LOCATION = "EEE"
    DEFAULT_USE_TIME_IN_HOURS = 24 * 365
    DEFAULT_WORKLOAD = 50.

    _DAYS_IN_HOURS = 24
    _YEARS_IN_HOURS = 24 * 365

    def __init__(self, /, **kwargs):
        self.__hours_electrical_consumption = self.DEFAULT_USE_TIME_IN_HOURS
        self.__workload = self.DEFAULT_WORKLOAD
        self.__usage_location = self.DEFAULT_USAGE_LOCATION
        self.__hours_use_time = self.DEFAULT_USE_TIME_IN_HOURS

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def hours_use_time(self) -> float:
        return self.__hours_use_time

    @hours_use_time.setter
    def hours_use_time(self, value: float) -> None:
        self.__hours_use_time = value

    @property
    def days_use_time(self) -> float:
        return self.hours_use_time / self._DAYS_IN_HOURS

    @days_use_time.setter
    def days_use_time(self, value: float) -> None:
        self.hours_use_time = value * self._DAYS_IN_HOURS

    @property
    def years_use_time(self):
        return self.hours_use_time / self._YEARS_IN_HOURS

    @years_use_time.setter
    def years_use_time(self, value: float) -> None:
        self.__hours_use_time = value * self._YEARS_IN_HOURS

    @property
    def usage_location(self) -> str:
        return self.__usage_location

    @usage_location.setter
    def usage_location(self, value: str) -> None:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == value]
        if len(sub) == 0:
            self.__usage_location = self.DEFAULT_USAGE_LOCATION
        else:
            self.__usage_location = value

    @property
    def gwp_factor(self) -> float:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == self.usage_location]
        return float(sub['gwp_emission_factor'])

    @property
    def adp_factor(self) -> float:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == self.usage_location]
        return float(sub['adpe_emission_factor'])

    @property
    def pe_factor(self) -> float:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == self.usage_location]
        return float(sub['pe_emission_factor'])

    @property
    def workload(self) -> Union[Dict[str, float], float]:
        return self.__workload

    @workload.setter
    def workload(self, value: Union[Dict[str, float], float]) -> None:
        self.__workload = value

    def get_duration_hours(self) -> float:
        return self.hours_use_time

    @property
    def hours_electrical_consumption(self) -> float:
        if not self.__hours_electrical_consumption:
            self.__hours_electrical_consumption = 0
        return self.__hours_electrical_consumption / 1000  # in kwh

    @classmethod
    def from_dto(cls, usage: Usage):
        return cls(**usage.dict())


class ModelUsageServer(ModelUsage):
    DEFAULT_OTHER_CONSUMPTION_RATIO = 0.33

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)

        self.__other_consumption_ratio = self.DEFAULT_OTHER_CONSUMPTION_RATIO

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def other_consumption_ratio(self) -> float:
        return self.__other_consumption_ratio

    @other_consumption_ratio.setter
    def other_consumption_ratio(self, value: float) -> None:
        self.__other_consumption_ratio = value


class ModelUsageCloud(ModelUsageServer):
    DEFAULT_INSTANCE_PER_SERVER = 1

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)

        self.__instance_per_server = self.DEFAULT_INSTANCE_PER_SERVER

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def instance_per_server(self) -> int:
        return self.__instance_per_server

    @instance_per_server.setter
    def instance_per_server(self, value: int) -> None:
        self.__instance_per_server = value
