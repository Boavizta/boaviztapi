from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.consumption_profile.consumption_profile import RAMConsumptionProfileModel
from boaviztapi.model.impact import ImpactFactor


class ComponentRAM(Component):
    NAME = "RAM"

    IMPACT_FACTOR = {
        'gwp': {
            'die_impact': 2.20,
            'impact': 5.22
        },
        'pe': {
            'die_impact': 27.30,
            'impact': 74.00
        },
        'adp': {
            'die_impact': 6.30E-05,
            'impact': 1.69E-03
        }
    }

    def __init__(self, default_config=config["DEFAULT"]["RAM"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)

        self.process = Boattribute(
            default=default_config['process']['default'],
            min=default_config['process']['min'],
            max=default_config['process']['max']
        )
        self.manufacturer = Boattribute(
            default=default_config['manufacturer']['default'],
        )
        self.capacity = Boattribute(
            unit="GB",
            default=default_config['capacity']['default'],
            min=default_config['capacity']['min'],
            max=default_config['capacity']['max']
        )
        self.density = Boattribute(
            unit="GB/cm2",
            default=default_config['density']['default'],
            min=default_config['density']['min'],
            max=default_config['density']['max']
        )

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        ram_die_impact, ram_impact = self.__get_impact_constants(impact_type)

        impact = self.__compute_impact_manufacture(ram_die_impact, ram_impact)

        sign_figures = self.__compute_significant_numbers(ram_die_impact.value, ram_impact.value)
        return impact.value, sign_figures, impact.min, impact.max, []

    def __impact_usage(self, impact_type: str) -> ComputedImpacts:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')

        if not self.usage.hours_electrical_consumption.is_set():
            modeled_consumption = self.model_power_consumption()
            self.usage.hours_electrical_consumption.set_completed(
                modeled_consumption.value,
                min=modeled_consumption.min,
                max=modeled_consumption.max
            )

            self.usage.hours_electrical_consumption.status = Status.COMPLETED

        impact = ImpactFactor(
            value=impact_factor.value * (
                    self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value,
            min=impact_factor.min * (
                    self.usage.hours_electrical_consumption.min / 1000) * self.usage.use_time.min,
            max=impact_factor.max * (
                    self.usage.hours_electrical_consumption.max / 1000) * self.usage.use_time.max
        )

        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)
        return impact.value, sig_fig, impact.min, impact.max, []

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value,
                                          impact_factor)

    def model_power_consumption(self,) -> ImpactFactor:
        self.usage.consumption_profile = RAMConsumptionProfileModel()
        self.usage.consumption_profile.compute_consumption_profile_model(ram_capacity=self.capacity.value)

        if type(self.usage.time_workload.value) in (float, int):
            self.usage.hours_electrical_consumption.set_completed(
                self.usage.consumption_profile.apply_consumption_profile(self.usage.time_workload.value))
        else:
            self.usage.hours_electrical_consumption.set_completed(
                self.usage.consumption_profile.apply_multiple_workloads(self.usage.time_workload.value))

        return ImpactFactor(
                value=rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5),
                min=rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5),
                max=rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5)
        )

    def __get_impact_constants(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor]:
        ram_die_impact = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['die_impact'],
            min=self.IMPACT_FACTOR[impact_type]['die_impact'],
            max=self.IMPACT_FACTOR[impact_type]['die_impact']
        )
        ram_impact = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['impact'],
            min=self.IMPACT_FACTOR[impact_type]['impact'],
            max=self.IMPACT_FACTOR[impact_type]['impact']
        )
        return ram_die_impact, ram_impact

    def __compute_significant_numbers(self, ram_die_impact: float, ram_impact: float) -> int:
        return rd.min_significant_figures(self.density.value, ram_die_impact, ram_impact)

    def __compute_impact_manufacture(self, ram_die_impact: ImpactFactor, ram_impact: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(self.capacity.value / self.density.value) * ram_die_impact.value + ram_impact.value,
            min=(self.capacity.min / self.density.min) * ram_die_impact.min + ram_impact.min,
            max=(self.capacity.max / self.density.max) * ram_die_impact.max + ram_impact.max
        )

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def impact_use_gwp(self) -> ComputedImpacts:
        return self.__impact_usage("gwp")

    def impact_use_pe(self) -> ComputedImpacts:
        return self.__impact_usage("pe")

    def impact_use_adp(self) -> ComputedImpacts:
        return self.__impact_usage("adp")