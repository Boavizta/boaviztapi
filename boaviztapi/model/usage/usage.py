import pandas as pd


from boaviztapi.dto.usage import Usage, UsageServer, UsageCloud
from boaviztapi.model.boattribute import Boattribute, Status

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

        self._hours_electrical_consumption = Boattribute(value=None, status=Status.NONE, unit="W")
        self._workload = None
        self._usage_location = Boattribute(value=None, status=Status.NONE, unit="CodSP3 - NCS Country Codes - NATO")
        self._adp_factor = Boattribute(value=None, status=Status.NONE, unit="..")
        self._gwp_factor = Boattribute(value=None, status=Status.NONE, unit="..")
        self._pe_factor = Boattribute(value=None, status=Status.NONE, unit="..")

        self._use_time = Boattribute(value=None, status=Status.NONE, unit="hours")

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

        if "days_use_time" in kwargs or "hours_use_time" in kwargs or "years_use_time" in kwargs:

            self.use_time = (kwargs.pop('hours_use_time') or 0) + \
                            (kwargs.pop('days_use_time') or 0) * self._DAYS_IN_HOURS + \
                            (kwargs.pop('years_use_time') or 0) * self._YEARS_IN_HOURS

            self._use_time.status = Status.INPUT

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    @property
    def use_time(self) -> float:
        if self._use_time.value == 0 or self._use_time.value is None:
            self._use_time.value = self.DEFAULT_USE_TIME_IN_HOURS
            self._use_time.status = Status.DEFAULT
        return self._use_time.value

    @use_time.setter
    def use_time(self, value: float) -> None:
        self._use_time.value = value

    @property
    def usage_location(self) -> str:
        if self._usage_location.value is None:
            self._usage_location.value = self.DEFAULT_USAGE_LOCATION
            self._usage_location.status = Status.DEFAULT
        return self._usage_location.value

    @usage_location.setter
    def usage_location(self, value: str) -> None:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == value]
        if len(sub) == 0:
            self._usage_location.value = self.DEFAULT_USAGE_LOCATION
            self._usage_location.status = Status.DEFAULT
        else:
            self._usage_location.value = value
            self._usage_location.status = Status.INPUT

    @property
    def gwp_factor(self) -> float:
        if self._gwp_factor.value is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self._gwp_factor.value = float(sub['gwp_emission_factor'])
            self._gwp_factor.status = Status.DEFAULT
        return self._gwp_factor.value

    @property
    def adp_factor(self) -> float:
        if self._adp_factor.value is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self._adp_factor.value = float(sub['adpe_emission_factor'])
            self._adp_factor.status = Status.DEFAULT
        return self._adp_factor.value

    @property
    def pe_factor(self) -> float:
        if self._pe_factor.value is None:
            sub = _electricity_emission_factors_df
            sub = sub[sub['code'] == self.usage_location]
            self._pe_factor.value = float(sub['pe_emission_factor'])
            self._pe_factor.status = Status.DEFAULT
        return self._pe_factor.value

    @gwp_factor.setter
    def gwp_factor(self, value):
        self._gwp_factor.value = value

    @adp_factor.setter
    def adp_factor(self, value):
        self._adp_factor.value = value

    @pe_factor.setter
    def pe_factor(self, value):
        self._pe_factor.value = value

    @property
    def hours_electrical_consumption(self) -> float:
        if self._hours_electrical_consumption.value is None:
            self._hours_electrical_consumption.value = 0
            self._hours_electrical_consumption.status = Status.DEFAULT
        return self._hours_electrical_consumption.value

    @hours_electrical_consumption.setter
    def hours_electrical_consumption(self, value):
        self._hours_electrical_consumption.value = value

    def _set_states_from_input(self, input_component_dto):
        for attr, val in input_component_dto.dict().items():
            if hasattr(self, f'_{attr}') and \
                    isinstance(self.__getattribute__(f'_{attr}'), Boattribute):
                if self.__getattribute__(f'_{attr}').value is None:
                    self.__getattribute__(f'_{attr}').status = Status.NONE
                elif val is not None and val != self.__getattribute__(f'_{attr}').value:
                    self.__getattribute__(f'_{attr}').status = Status.CHANGED
                elif val is None and self.__getattribute__(f'_{attr}') is not None:
                    self.__getattribute__(f'_{attr}').status = Status.COMPLETED
                elif val == self.__getattribute__(f'_{attr}').value:
                    self.__getattribute__(f'_{attr}').status = Status.INPUT


class ModelUsageServer(ModelUsage):
    DEFAULT_OTHER_CONSUMPTION_RATIO = 0.33

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)

        self._other_consumption_ratio = Boattribute(value=None, status=Status.NONE, unit="ratio /1")

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def other_consumption_ratio(self) -> float:
        if self._other_consumption_ratio.value is None:
            self._other_consumption_ratio.value = self.DEFAULT_OTHER_CONSUMPTION_RATIO
            self._other_consumption_ratio.status = Status.DEFAULT
        return self._other_consumption_ratio.value

    @other_consumption_ratio.setter
    def other_consumption_ratio(self, value: float) -> None:
        self._other_consumption_ratio.value = value

    @classmethod
    def from_dto(cls, usage_server_complete: UsageServer, usage_server_input: UsageServer):
        usage_ = cls(**usage_server_complete.dict())
        usage_._set_states_from_input(usage_server_input)
        return usage_


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

    @classmethod
    def from_dto(cls, usage_cloud_complete: UsageCloud, usage_cloud_input: UsageCloud):
        return super().from_dto(usage_cloud_complete, usage_cloud_input)
