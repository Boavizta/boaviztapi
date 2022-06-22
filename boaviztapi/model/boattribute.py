from enum import Enum


class Boattribute:
    def __init__(self, /, **kwargs):

        self.value = None
        self.unit = None
        self.status = None
        self.source = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)


class Status(Enum):
    NONE = "NONE"
    INPUT = "INPUT"
    COMPLETED = "COMPLETED"
    DEFAULT = "DEFAULT"
    CHANGED = "CHANGED"
