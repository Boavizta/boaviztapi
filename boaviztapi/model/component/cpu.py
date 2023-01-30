from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel


class ComponentCPU(Component):
    NAME = "CPU"

    IMPACT_FACTOR = {
        'gwp': {
            'die_impact': 1.97,
            'impact': 9.14
        },
        'pe': {
            'die_impact': 26.50,
            'impact': 156.00
        },
        'adp': {
            'die_impact': 5.80E-07,
            'impact': 2.04E-02
        },
        'constant_core_impact': 0.491
    }

    def __init__(self, default_config=config["DEFAULT"]["CPU"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)
        self.core_units = Boattribute(
            default=default_config['core_units']['default'],
            min=default_config['core_units']['min'],
            max=default_config['core_units']['max']
        )
        self.die_size_per_core = Boattribute(
            unit="mm2",
            default=default_config['die_size_per_core']['default'],
            min=default_config['die_size_per_core']['min'],
            max=default_config['die_size_per_core']['max']
        )
        self.model_range = Boattribute(
            default=default_config['model_range']['default'],
        )
        self.manufacturer = Boattribute(
            default=default_config['manufacturer']['default'],
        )
        self.family = Boattribute(
            default=default_config['manufacturer']['default'],
        )
        self.tdp = Boattribute(
            unit="W",
            default=default_config['tdp']['default'],
            min=default_config['tdp']['min'],
            max=default_config['tdp']['max']
        )

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        core_impact, cpu_die_impact, cpu_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(core_impact, cpu_die_impact, cpu_impact)
        impact = self.__compute_impact_manufacture(core_impact, cpu_die_impact, cpu_impact)
        return impact, sign_figures, 0, []

    def __impact_usage(self, impact_type: str) -> ComputedImpacts:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')

        if not self.usage.hours_electrical_consumption.is_set():
            self.usage.hours_electrical_consumption.value = self.model_power_consumption()
            self.usage.hours_electrical_consumption.status = Status.COMPLETED

        impacts = impact_factor.value * (
                self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value

        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)
        return impacts, sig_fig, 0, []

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value,
                                          impact_factor)

    def model_power_consumption(self):
        self.usage.consumption_profile = CPUConsumptionProfileModel()

        manuf, model, tdp = None, None, None
        if self.manufacturer.is_set(): manuf = self.manufacturer.value
        if self.model_range.is_set(): model = self.model_range.value
        if self.tdp.is_set(): tdp = self.tdp.value

        self.usage.consumption_profile.compute_consumption_profile_model(cpu_manufacturer=manuf,
                                                                         cpu_model_range=model,
                                                                         cpu_tdp=tdp)
        if type(self.usage.time_workload.value) == float:
            self.usage.hours_electrical_consumption.set_completed(self.usage.consumption_profile.apply_consumption_profile(self.usage.time_workload.value))
        else:
            self.usage.hours_electrical_consumption.set_completed(self.usage.consumption_profile.apply_multiple_workloads(self.usage.time_workload.value))

        return rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5)

    def __get_impact_constants(self, impact_type: str) -> Tuple[float, float, float]:
        core_impact = self.IMPACT_FACTOR['constant_core_impact']
        cpu_die_impact = self.IMPACT_FACTOR[impact_type]['die_impact']
        cpu_impact = self.IMPACT_FACTOR[impact_type]['impact']
        return core_impact, cpu_die_impact, cpu_impact

    def __compute_significant_numbers(self, core_impact: float, cpu_die_impact: float, cpu_impact: float) -> int:
        return rd.min_significant_figures(self.die_size_per_core.value, core_impact, cpu_die_impact, cpu_impact)

    def __compute_impact_manufacture(self, core_impact: float, cpu_die_impact: float, cpu_impact: float) -> float:
        return (self.core_units.value * self.die_size_per_core.value + core_impact) * cpu_die_impact + cpu_impact

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> ComputedImpacts:
        return self.__impact_usage("gwp")

    def impact_use_pe(self) -> ComputedImpacts:
        return self.__impact_usage("pe")

    def impact_use_adp(self) -> ComputedImpacts:
        return self.__impact_usage("adp")
