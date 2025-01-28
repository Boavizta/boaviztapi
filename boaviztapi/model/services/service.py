from abc import ABC, abstractmethod
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.impact import Assessable
from boaviztapi.model.usage.usage import ModelUsage


class Service(Assessable, ABC):
    def __init__(self, archetype=None, **kwargs):
        super().__init__(**kwargs)
        self.units = Boattribute(default=1, min=1, max=1)
        self.archetype = archetype
        self._usage = None
        self._impacts = {}

    @property
    def usage(self) -> ModelUsage:
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value
