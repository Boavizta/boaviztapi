from abc import abstractmethod
from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi.model.usage import ModelUsage

NumberSignificantFigures = Tuple[float, int]


class Component:
    NAME = "COMPONENT"

    def __init__(self, **kwargs):
        self._units = None
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

    @property
    def units(self) -> int:
        if self._units is None:
            self._units = 1
        return self._units

    @units.setter
    def units(self, value: int) -> None:
        self._units = value

    def __impact_usage(self, impact_type: str) -> NumberSignificantFigures:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')

        impacts = impact_factor.value * (
                self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value
        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)
        return impacts, sig_fig

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value,
                                          impact_factor)

    @abstractmethod
    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_gwp(self) -> NumberSignificantFigures:
        return self.__impact_usage("gwp")

    def impact_use_pe(self) -> NumberSignificantFigures:
        return self.__impact_usage("pe")

    def impact_use_adp(self) -> NumberSignificantFigures:
        return self.__impact_usage("adp")
