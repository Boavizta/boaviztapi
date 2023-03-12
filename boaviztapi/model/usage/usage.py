import os

import pandas as pd

from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.impact import IMPACT_CRITERIAS

_electricity_emission_factors_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), '../../data/electricity/electricity_impact_factors.csv'))

_cpu_profile_path = os.path.join(os.path.dirname(__file__), '../../data/consumption_profile/cpu/cpu_profile.csv')
_cloud_profile_path = os.path.join(os.path.dirname(__file__), '../../data/consumption_profile/cloud/cpu_profile.csv')
_server_profile_path = os.path.join(os.path.dirname(__file__),
                                    '../../data/consumption_profile/server/server_profile.csv')

class ModelUsage:

    _DAYS_IN_HOURS = 24
    _YEARS_IN_HOURS = 24 * 365

    def __init__(self, default_config=config["DEFAULT"]["USAGE"], **kwargs):
        self.hours_electrical_consumption = Boattribute(
            unit="W",
            default=default_config['hours_electrical_consumption']['default'],
            min=default_config['hours_electrical_consumption']['min'],
            max=default_config['hours_electrical_consumption']['max']
        )
        self.time_workload = Boattribute(
            unit="%",
            default=default_config['time_workload']['default'],
            min=default_config['time_workload']['min'],
            max=default_config['time_workload']['max']
        )
        self.consumption_profile = None
        self.usage_location = Boattribute(
            unit="CodSP3 - NCS Country Codes - NATO",
            default=default_config['usage_location']['default']
        )
        self.adp_factor = Boattribute(
            unit="KgSbeq/kWh",
            complete_function=self._complete_impact_factor
        )

        self.gwp_factor = Boattribute(
            unit="kgCO2e/kWh",
            complete_function=self._complete_impact_factor
        )

        self.pe_factor = Boattribute(
            unit="MJ/kWh",
            complete_function=self._complete_impact_factor
        )

        self.use_time = Boattribute(
            unit="hours",
            default=default_config['use_time']['default'],
            min=default_config['use_time']['min'],
            max=default_config['use_time']['max']
        )
        self.life_time = Boattribute(
            unit="hours",
            default=default_config['life_time']['default'],
            min=default_config['life_time']['min'],
            max=default_config['life_time']['max']
        )

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def _complete_impact_factor(self):
        sub = _electricity_emission_factors_df
        sub_selected = sub[sub['code'] == self.usage_location.value]

        for i in IMPACT_CRITERIAS:
            column_value = f"{i.name}_emission_factor" if i.name != "adp" else "adpe_emission_factor"
            column_source = f"{i.name}_emission_source" if i.name != "adp" else "adpe_emission_source"
            factor = float(sub_selected[column_value].iloc[0])

            if self.usage_location.is_default():
                getattr(self, f"{i.name}_factor").set_default(factor, source=str(sub_selected[column_source].iloc[0]))
                getattr(self, f"{i.name}_factor").min = float(sub[column_value].min())
                getattr(self, f"{i.name}_factor").max = float(sub[column_value].max())
            else:
                getattr(self, f"{i.name}_factor").set_completed(factor,
                                                                source=str(sub_selected[column_source].iloc[0]),
                                                                min=factor, max=factor)

class ModelUsageServer(ModelUsage):

    def __init__(self, default_config=config["SERVER"]["USAGE"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)

        self.other_consumption_ratio = Boattribute(
            unit="ratio /1",
            default=default_config['other_consumption_ratio']['default'],
            min=default_config['other_consumption_ratio']['min'],
            max=default_config['other_consumption_ratio']['max']
        )

class ModelUsageCloud(ModelUsageServer):
    def __init__(self, default_config=config["CLOUD"]["USAGE"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)
        self.instance_per_server = Boattribute(
            default=default_config['instance_per_server']['default'],
            min=default_config['instance_per_server']['min'],
            max=default_config['instance_per_server']['max']
        )

