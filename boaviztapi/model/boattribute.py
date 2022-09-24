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

        self._value = None
        self.unit = "none"
        self.status = Status.NONE
        self.source = None
        self.default = None
        self.args = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def value(self) -> Any:
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
    def value(self, value: Any):
        self._value = value

    def to_json(self):
        json = {"value": self._value, "unit": self.unit, "status": self.status.value, "source": self.source}
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
        self.__set_value_and_status(value, Status.INPUT, source)

    def set_completed(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.COMPLETED, source)

    def set_default(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.DEFAULT, source)

    def set_changed(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.CHANGED, source)

    def set_archetype(self, value: Any, *, source: Optional[str] = None) -> None:
        self.__set_value_and_status(value, Status.ARCHETYPE, source)

    def __set_value_and_status(self, value: Any, status: Status, source: str) -> None:
        self._value = value
        self.status = status
        if source is not None:
            self.source = source
