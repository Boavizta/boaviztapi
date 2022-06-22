from abc import abstractmethod
from typing import Tuple
from uuid import UUID

from boaviztapi.dto.component import ComponentDTO
from boaviztapi.model.boattribute import Status

NumberSignificantFigures = Tuple[float, int]


class Component:

    def __init__(self, **kwargs):
        pass

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

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
    def from_dto(cls, completed_component_dto: ComponentDTO, input_component_dto: ComponentDTO = ComponentDTO()) -> 'Component':
        component = cls(**completed_component_dto.dict())
        component._set_states_from_input(input_component_dto)
        return component

    @abstractmethod
    def to_dto(self, original_component: ComponentDTO) -> ComponentDTO:
        raise NotImplementedError

    def _set_states_from_input(self, input_component_dto):
        class_name = self.__class__.__name__
        for attr, val in input_component_dto.dict().items():
            if hasattr(self, f'_{class_name}__{attr}'):
                if self.__getattribute__(f'_{class_name}__{attr}').value is None:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.NONE
                elif val is not None and val != self.__getattribute__(f'_{class_name}__{attr}').value:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.CHANGED
                elif val is None and self.__getattribute__(f'_{class_name}__{attr}') is not None:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.COMPLETED
                elif val == self.__getattribute__(f'_{class_name}__{attr}').value:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.INPUT
