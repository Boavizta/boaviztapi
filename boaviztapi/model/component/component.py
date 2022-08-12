from abc import abstractmethod
from typing import Tuple

from boaviztapi.model.consumption_profile.consumption_profile import ConsumptionProfileModel
from boaviztapi.model.usage import ModelUsage

NumberSignificantFigures = Tuple[float, int]


class Component:
    NAME = "COMPONENT"

    def __init__(self, **kwargs):
        self._units = None
        self._usage = None
        self._consumption_profile = None

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

    @abstractmethod
    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_use_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_use_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @abstractmethod
    def impact_use_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError
