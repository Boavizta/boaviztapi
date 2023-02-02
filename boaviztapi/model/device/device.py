from abc import abstractmethod
from typing import Tuple, List

from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component import Component
from boaviztapi.model.usage import ModelUsage

ComputedImpacts = Tuple[float, int]


class Device:

    def __init__(self, **kwargs):
        self.units = Boattribute(
            default=1,
            min=1,
            max=1
        )
        self._usage = None
        pass

    @property
    def usage(self) -> ModelUsage:
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value

    @property
    def components(self) -> List[Component]:
        return []

    @abstractmethod
    def impact_manufacture_gwp(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_pe(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_manufacture_adp(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_use_gwp(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_use_pe(self) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_use_adp(self) -> ComputedImpacts:
        raise NotImplementedError

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

