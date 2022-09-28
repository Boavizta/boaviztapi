from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, NumberSignificantFigures
from boaviztapi.model.consumption_profile.consumption_profile import RAMConsumptionProfileModel


class ComponentRAM(Component):
    NAME = "RAM"

    DEFAULT_RAM_CAPACITY = 32
    DEFAULT_RAM_DENSITY = 0.625
    DEFAULT_RAM_PROCESS = 30
    DEFAULT_RAM_MANUFACTURER = "Samsung"

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.process = Boattribute(default=self.DEFAULT_RAM_PROCESS)
        self.manufacturer = Boattribute(default=self.DEFAULT_RAM_MANUFACTURER)
        self.capacity = Boattribute(
            unit="GB",
            default=self.DEFAULT_RAM_CAPACITY
        )
        self.density = Boattribute(
            unit="GB/cm2",
            default=self.DEFAULT_RAM_DENSITY
        )

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        ram_die_impact, ram_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(ram_die_impact, ram_impact)
        impact = self.__compute_impact_manufacture(ram_die_impact, ram_impact)
        return impact, sign_figures

    def __impact_usage(self, impact_type: str) -> NumberSignificantFigures:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')

        if not self.usage.hours_electrical_consumption.is_set():
            self.usage.hours_electrical_consumption.value = self.model_power_consumption()
            self.usage.hours_electrical_consumption.status = Status.COMPLETED

        impacts = impact_factor.value * (self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value

        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)
        return impacts, sig_fig

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value,
                                          impact_factor)

    def model_power_consumption(self):
        self.usage.consumption_profile = RAMConsumptionProfileModel()
        self.usage.consumption_profile.compute_consumption_profile_model(ram_capacity=self.capacity.value)

        if type(self.usage.time_workload.value) == float:
            self.usage.hours_electrical_consumption.set_completed(
                self.usage.consumption_profile.apply_consumption_profile(self.usage.time_workload.value))
        else:
            self.usage.hours_electrical_consumption.set_completed(
                self.usage.consumption_profile.apply_multiple_workloads(self.usage.time_workload.value))

        return self.usage.hours_electrical_consumption.value

    def __get_impact_constants(self, impact_type: str) -> Tuple[float, float]:
        ram_die_impact = self.IMPACT_FACTOR[impact_type]['die_impact']
        ram_impact = self.IMPACT_FACTOR[impact_type]['impact']
        return ram_die_impact, ram_impact

    def __compute_significant_numbers(self, ram_die_impact: float, ram_impact: float) -> int:
        return rd.min_significant_figures(self.density.value, ram_die_impact, ram_impact)

    def __compute_impact_manufacture(self, ram_die_impact: float, ram_impact: float) -> float:
        return (self.capacity.value / self.density.value) * ram_die_impact + ram_impact

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> NumberSignificantFigures:
        return self.__impact_usage("gwp")

    def impact_use_pe(self) -> NumberSignificantFigures:
        return self.__impact_usage("pe")

    def impact_use_adp(self) -> NumberSignificantFigures:
        return self.__impact_usage("adp")