import os

import pandas as pd

from boaviztapi import config, data_dir
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.impact import IMPACT_CRITERIAS
from boaviztapi.service.archetype import get_arch_value, get_server_archetype, get_cloud_instance_archetype

_electricity_emission_factors_df = pd.read_csv(os.path.join(data_dir, 'electricity/electricity_impact_factors.csv'))

_cpu_profile_path = os.path.join(data_dir, 'consumption_profile/cpu/cpu_profile.csv')
_cloud_profile_path = os.path.join(data_dir, 'consumption_profile/cloud/cpu_profile.csv')
_server_profile_path = os.path.join(data_dir, 'consumption_profile/server/server_profile.csv')

class ModelUsage:

    _DAYS_IN_HOURS = 24
    _YEARS_IN_HOURS = 24 * 365

    def __init__(self, archetype, **kwargs):
        self.archetype = archetype
        self.hours_electrical_consumption = Boattribute(
            unit="W",
            default=get_arch_value(archetype, 'hours_electrical_consumption', 'default'),
            min=get_arch_value(archetype, 'hours_electrical_consumption', 'min'),
            max=get_arch_value(archetype, 'hours_electrical_consumption', 'max')
        )
        self.time_workload = Boattribute(
            unit="%",
            default=get_arch_value(archetype, 'time_workload', 'default'),
            min=get_arch_value(archetype, 'time_workload', 'min'),
            max=get_arch_value(archetype, 'time_workload', 'max')
        )
        self.consumption_profile = None
        self.usage_location = Boattribute(
            unit="CodSP3 - NCS Country Codes - NATO",
            default=get_arch_value(archetype, 'usage_location', 'default'),
            min=get_arch_value(archetype, 'usage_location', 'min'),
            max=get_arch_value(archetype, 'usage_location', 'max')
        )
        self.use_time = Boattribute(
            unit="hours",
            default=get_arch_value(archetype, 'use_time', 'default'),
            min=get_arch_value(archetype, 'use_time', 'min'),
            max=get_arch_value(archetype, 'use_time', 'max')
        )
        self.life_time = Boattribute(
            unit="hours",
            default=get_arch_value(archetype, 'life_time', 'default'),
            min=get_arch_value(archetype, 'life_time', 'min'),
            max=get_arch_value(archetype, 'life_time', 'max')
        )
        self.elec_factors = {
            "gwp": Boattribute(unit="kg CO2eq/kWh", complete_function=self._complete_gwp),
            "adp": Boattribute(unit="kg Sbeq/kWh", complete_function=self._complete_adp),
            "pe": Boattribute(unit="MJ/kWh", complete_function=self._complete_pe),
            "gwppb": Boattribute(unit="kg CO2eq/kWh", complete_function=self._complete_gwppb),
            "gwppf": Boattribute(unit="kg CO2eq/kWh", complete_function=self._complete_gwppf),
            "gwpplu": Boattribute(unit="kg CO2eq/kWh", complete_function=self._complete_gwpplu),
            "ir": Boattribute(unit="kg U235eq/kWh", complete_function=self._complete_ir),
            "lu": Boattribute(unit="No dimension/kWh", complete_function=self._complete_lu),
            "odp": Boattribute(unit="kg CFC-11eq/kWh", complete_function=self._complete_odp),
            "pm": Boattribute(unit="Disease occurrence/kWh", complete_function=self._complete_pm),
            "pocp": Boattribute(unit="kg NMVOCeq/kWh", complete_function=self._complete_pocp),
            "wu": Boattribute(unit="m3eq/kWh", complete_function=self._complete_wu),
            "mips": Boattribute(unit="kg/kWh", complete_function=self._complete_mips),
            "adpe": Boattribute(unit="kg Sbeq/kWh", complete_function=self._complete_adpe),
            "adpf": Boattribute(unit="MJ/kWh", complete_function=self._complete_adpf),
            "ap": Boattribute(unit="mol H+eq/kWh", complete_function=self._complete_ap),
            "ctue": Boattribute(unit="CTUe/kWh", complete_function=self._complete_ctue),
            "ctuh_c": Boattribute(unit="CTUh/kWh", complete_function=self._complete_ctuh_c),
            "ctuh_nc": Boattribute(unit="CTUh/kWh", complete_function=self._complete_ctuh_nc),
            "epf": Boattribute(unit="kg Peq/kWh", complete_function=self._complete_epf),
            "epm": Boattribute(unit="kg Neq/kWh", complete_function=self._complete_epm),
            "ept": Boattribute(unit="mol Neq/kWh", complete_function=self._complete_ept),
        }

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def _complete_impact_factor(self, impact_criteria, column_name):
        if column_name is None:
            raise NotImplementedError

        sub = _electricity_emission_factors_df
        if not self.usage_location.has_value():
            self.usage_location.set_default(config["default_location"])

        sub_selected = sub[sub['code'] == self.usage_location.value]

        column_value = f"{column_name}_emission_factor"
        column_source = f"{column_name}_emission_source"

        if not column_value in sub.columns:
            raise NotImplementedError

        factor = float(sub_selected[column_value].iloc[0])

        if self.usage_location.is_default():
            self.elec_factors.get(impact_criteria).set_default(factor, source=str(sub_selected[column_source].iloc[0]))
            self.elec_factors.get(impact_criteria).min = float(sub[column_value].min())
            self.elec_factors.get(impact_criteria).max = float(sub[column_value].max())
        else:
            self.elec_factors.get(impact_criteria).set_completed(factor,
                                                             source=str(sub_selected[column_source].iloc[0]),
                                                             min=factor, max=factor)

    def _complete_gwp(self):
        self._complete_impact_factor("gwp", "gwp")
    def _complete_adp(self):
        self._complete_impact_factor("adp", "adpe")
    def _complete_pe(self):
        self._complete_impact_factor("pe", "pe")
    def _complete_gwppb(self):
        self._complete_impact_factor("gwppb", None)
    def _complete_gwppf(self):
        self._complete_impact_factor("gwppf", None)
    def _complete_gwpplu(self):
        self._complete_impact_factor("gwpplu", None)
    def _complete_ir(self):
        self._complete_impact_factor("ir", None)
    def _complete_lu(self):
        self._complete_impact_factor("lu", None)
    def _complete_odp(self):
        self._complete_impact_factor("odp", None)
    def _complete_pm(self):
        self._complete_impact_factor("pm", None)
    def _complete_pocp(self):
        self._complete_impact_factor("pocp", None)
    def _complete_wu(self):
        self._complete_impact_factor("wu", None)
    def _complete_mips(self):
        self._complete_impact_factor("mips", None)
    def _complete_adpe(self):
        self._complete_impact_factor("adpe", "adpe")
    def _complete_adpf(self):
        self._complete_impact_factor("adpf", None)
    def _complete_ap(self):
        self._complete_impact_factor("ap", None)
    def _complete_ctue(self):
        self._complete_impact_factor("ctue", None)
    def _complete_ctuh_c(self):
        self._complete_impact_factor("ctuh_c", None)
    def _complete_ctuh_nc(self):
        self._complete_impact_factor("ctuh_nc", None)
    def _complete_epf(self):
        self._complete_impact_factor("epf", None)
    def _complete_epm(self):
        self._complete_impact_factor("epm", None)
    def _complete_ept(self):
        self._complete_impact_factor("ept", None)

class ModelUsageServer(ModelUsage):

    def __init__(self, archetype=get_server_archetype(config["default_server"]).get("USAGE"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self.other_consumption_ratio = Boattribute(
            unit="ratio /1",
            default=get_arch_value(archetype, 'other_consumption_ratio', 'default'),
            min=get_arch_value(archetype, 'other_consumption_ratio', 'min'),
            max=get_arch_value(archetype, 'other_consumption_ratio', 'max')
        )

class ModelUsageCloud(ModelUsageServer):
    def __init__(self, archetype=get_cloud_instance_archetype(config["default_cloud"], config["default_cloud_provider"]).get("USAGE"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.instance_per_server = Boattribute(
            default=get_arch_value(archetype, 'instance_per_server', 'default'),
            min=get_arch_value(archetype, 'instance_per_server', 'min'),
            max=get_arch_value(archetype, 'instance_per_server', 'max')
        )