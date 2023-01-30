import os

import pandas as pd

from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute, Status

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
            default=default_impact_factor,
            args={"impact_type": "adpe",
                  "usage_location": self.usage_location,
                  "emission_factors_df": _electricity_emission_factors_df})
        self.gwp_factor = Boattribute(
            unit="kgCO2e/kWh",
            default=default_impact_factor,
            args={"impact_type": "gwp",
                  "usage_location": self.usage_location,
                  "emission_factors_df": _electricity_emission_factors_df})
        self.pe_factor = Boattribute(
            unit="MJ/kWh",
            default=default_impact_factor,
            args={"impact_type": "pe",
                  "usage_location": self.usage_location,
                  "emission_factors_df": _electricity_emission_factors_df})

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


class ModelUsageServer(ModelUsage):

    def __init__(self, default_config=config["DEFAULT"]["USAGE"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)

        self.other_consumption_ratio = Boattribute(
            unit="ratio /1",
            default=default_config.other_consumption_ratio.default,
            min=default_config.other_consumption_ratio.min,
            max=default_config.other_consumption_ratio.max
        )


class ModelUsageCloud(ModelUsageServer):
    def __init__(self, default_config=config["DEFAULT"]["USAGE"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)
        self.instance_per_server = Boattribute(
            default=default_config['instance_per_server']['default'],
            min=default_config['instance_per_server']['min'],
            max=default_config['instance_per_server']['max']
        )


def default_impact_factor(args):
    sub = args["emission_factors_df"]
    sub = sub[sub['code'] == args["usage_location"].value]
    return float(sub[f"{args['impact_type']}_emission_factor"]), sub[
        f"{args['impact_type']}_emission_source"].iloc[0], Status.COMPLETED
