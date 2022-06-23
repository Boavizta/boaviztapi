from abc import abstractmethod
from typing import Tuple, Union, List

from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.device import DeviceDTO
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.component import Component
from boaviztapi.model.usage import ModelUsage

NumberSignificantFigures = Tuple[float, int]


class Device:

    def __init__(self, /, **kwargs):
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

    @abstractmethod
    def to_dto(self, original_device: DeviceDTO) -> DeviceDTO:
        raise NotImplementedError

    def _set_states_from_input(self, input_component_dto):
        class_name = self.__class__.__name__
        for attr, val in input_component_dto.dict().items():
            if hasattr(self, f'_{class_name}__{attr}') and \
                    isinstance(self.__getattribute__(f'_{class_name}__{attr}'), Boattribute):
                if self.__getattribute__(f'_{class_name}__{attr}').value is None:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.NONE
                elif val is not None and val != self.__getattribute__(f'_{class_name}__{attr}').value:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.CHANGED
                elif val is None and self.__getattribute__(f'_{class_name}__{attr}') is not None:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.COMPLETED
                elif val == self.__getattribute__(f'_{class_name}__{attr}').value:
                    self.__getattribute__(f'_{class_name}__{attr}').status = Status.INPUT

    @classmethod
    def from_dto(cls, complete_complete_device_dto, input_complete_device_dto):
        pass
