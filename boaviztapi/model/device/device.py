from abc import abstractmethod
from typing import Tuple, List

from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component import Component
from boaviztapi.model.usage import ModelUsage


class Device:

    def __init__(self, archetype=None, **kwargs):
        self.impact_factor = {}
        self.archetype = archetype
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
    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        raise NotImplementedError

    @abstractmethod
    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        raise NotImplementedError

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
