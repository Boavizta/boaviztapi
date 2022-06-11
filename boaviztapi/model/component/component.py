from abc import abstractmethod
from typing import Tuple
from uuid import UUID

from boaviztapi.dto.component import ComponentDTO

NumberSignificantFigures = Tuple[float, int]


class Component:

    def __init__(self, **kwargs):
        self.__id = kwargs.get('__id', UUID('00000000-0000-0000-0000-000000000000'))

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    @property
    def id(self) -> UUID:
        return self.__id

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
    def from_dto(cls, component_dto: ComponentDTO) -> 'Component':
        raise NotImplementedError

    @abstractmethod
    def to_dto(self, original_component: ComponentDTO) -> ComponentDTO:
        raise NotImplementedError
