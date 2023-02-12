from abc import abstractmethod

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.usage import ModelUsage




class Component:
    NAME = "COMPONENT"

    def __init__(self, default_config=config["DEFAULT"]["COMPONENT"], **kwargs):
        self.units = Boattribute(
            default=default_config['units']['default'],
            min=default_config['units']['min'],
            max=default_config['units']['max']
        )
        self._usage = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    @property
    def usage(self) -> ModelUsage:
        if self._usage is None:
            self._usage = ModelUsage()
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value

    def __impact_usage(self, impact_type: str) -> ComputedImpacts:
        if not self.usage.hours_electrical_consumption.is_set():
            raise NotImplementedError
        impact_factor = getattr(self.usage, f'{impact_type}_factor')

        impacts = impact_factor.value * (
                self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value
        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)

        max_impact = impact_factor.max * (self.usage.hours_electrical_consumption.max / 1000) * self.usage.use_time.max
        min_impact = impact_factor.min * (self.usage.hours_electrical_consumption.min / 1000) * self.usage.use_time.min


        return impacts, sig_fig, min_impact, max_impact, []

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value,
                                          impact_factor)

    @abstractmethod
    def impact_manufacture_gwp(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_pe(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_adp(self) -> ComputedImpacts:
        raise NotImplementedError

    def impact_use_gwp(self) -> ComputedImpacts:
        return self.__impact_usage("gwp")

    def impact_use_pe(self) -> ComputedImpacts:
        return self.__impact_usage("pe")

    def impact_use_adp(self) -> ComputedImpacts:
        return self.__impact_usage("adp")
