from enum import Enum


class Boattribute:
    def __init__(self, **kwargs):

        self._value = None
        self.unit = None
        self.status = None
        self.source = None
        self.default = None
        self.args = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def value(self):
        if self._value is None:
            if callable(self.default):
                default = self.default(self.args)
                self._value = default[0]
                self.source = default[1]
                self.status = default[2]

            else:
                self._value = self.default
                self.status = Status.DEFAULT
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def to_json(self):
        json = {"value": self._value, "unit": self.unit, "status": self.status.value, "source": self.source}
        return json


class Status(Enum):
    NONE = "NONE"
    INPUT = "INPUT"
    COMPLETED = "COMPLETED"
    DEFAULT = "DEFAULT"
    CHANGED = "CHANGED"
    ARCHETYPE = "ARCHETYPE"
