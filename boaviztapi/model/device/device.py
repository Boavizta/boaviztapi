from abc import abstractmethod
from typing import Tuple

from boaviztapi.dto.device import DeviceDTO


NumberSignificantFigures = Tuple[float, int]


class Device:

    def __init__(self, /, **kwargs):
        pass

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

    @classmethod
    def from_dto(cls, device: DeviceDTO) -> 'Device':
        raise NotImplementedError
