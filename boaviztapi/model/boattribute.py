from enum import Enum
from typing import Any, Optional


class Status(Enum):
    NONE = "NONE"
    INPUT = "INPUT"
    COMPLETED = "COMPLETED"
    DEFAULT = "DEFAULT"
    CHANGED = "CHANGED"
    ARCHETYPE = "ARCHETYPE"


class Boattribute:
    def __init__(self, **kwargs):

        self._min = None
        self._max = None
        self._value = None
        self.unit = None
        self.status = Status.NONE
        self.source = None
        self.default = None
        self.args = None
        self.warnings = []
        self.complete_function = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def value(self) -> Any:
        if self._value is None:
            if self.complete_function:
                self.complete_function()
            if self._value is None and self.default is not None:
                self._value = self.default
                self.status = Status.ARCHETYPE
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    @property
    def min(self) -> Any:
        if self._min is None:
            self._min = self._value
        return self._min

    @min.setter
    def min(self, value: Any):
        self._min = value

    @property
    def max(self) -> Any:
        if self._max is None:
            self._max = self._value
        return self._max

    @max.setter
    def max(self, value: Any):
        self._max = value

    def add_warning(self, warn):
        self.warnings.append(warn)

    def to_json(self):
        json = {"value": self._value, "status": self.status.value}
        if self.unit: json['unit'] = self.unit
        if self.source: json['source'] = self.source
        if (self._min or self._min==0) and (self.is_default() or self.is_completed() or self.is_archetype()): json['min'] = self._min
        if (self._max or self._max==0) and (self.is_default() or self.is_completed() or self.is_archetype()): json['max'] = self._max
        if self.warnings: json['warnings'] = self.warnings

        return json

    def is_set(self):
        return self.status != Status.NONE

    def is_none(self):
        return self.status == Status.NONE

    def is_input(self):
        return self.status == Status.INPUT

    def is_default(self):
        return self.status == Status.DEFAULT

    def is_completed(self):
        return self.status == Status.COMPLETED

    def is_changed(self):
        return self.status == Status.CHANGED

    def is_archetype(self):
        return self.status == Status.ARCHETYPE

    def set_input(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.INPUT, source, min=value, max=value)

    def set_completed(self, value: Any, *, source: Optional[str] = None, min = None, max = None) -> None:
        self.__set_value_and_status(value, Status.COMPLETED, source, min=min, max=max)

    def set_default(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.DEFAULT, source)

    def set_changed(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.CHANGED, source)

    def set_archetype(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.ARCHETYPE, source)

    def __set_value_and_status(self, value: Any, status: Status, source: str, min:float = None, max:float=None) -> None:
        self._value = value
        self.status = status
        if source is not None:
            self.source = source
        if min is not None:
            self.min = min
        if max is not None:
            self.max = max

    def has_value(self):
        return (self._value is not None) or (self.default is not None)


