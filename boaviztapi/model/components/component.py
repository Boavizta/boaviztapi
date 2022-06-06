import hashlib
from abc import abstractmethod, ABC
from typing import Tuple

from boaviztapi.dto.components import ComponentDTO

NumberSignificantFigures = Tuple[float, int]


class Component:

    def __init__(self, /, **kwargs):
        self.hash = self.__hash__()

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __hash__(self):
        object_fingerprint = bytes(((type(self),) + tuple(self.__dict__.values())).__str__(), encoding='utf8')
        return hashlib.sha256(object_fingerprint).hexdigest()

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

    @classmethod
    def from_dto(cls, arg: ComponentDTO) -> 'Component':
        raise NotImplementedError
