from typing import List

from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component import Component
from boaviztapi.models.impact import Assessable
from boaviztapi.models.usage import ModelUsage


class Device(Assessable):
    NAME = None

    def __init__(self, archetype=None, **kwargs):
        super().__init__(**kwargs)
        self.archetype = archetype
        self.type = None
        self.units = Boattribute(default=1, min=1, max=1)
        self._usage = None
        self._impacts = {}

    @property
    def usage(self) -> ModelUsage:
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value

    @property
    def components(self) -> List[Component]:
        return []

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
