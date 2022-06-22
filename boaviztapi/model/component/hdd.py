import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, NumberSignificantFigures
from boaviztapi.dto.component import Disk


class ComponentHDD(Component):
    NAME = "HDD"

    __DISK_TYPE = 'hdd'

    DEFAULT_HDD_CAPACITY = 500

    IMPACT_FACTOR = {
        'gwp': {
            'impact': 31.10
        },
        'pe': {
            'impact': 276.00
        },
        'adp': {
            'impact': 2.50E-04
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__capacity = Boattribute(value=None, status=Status.NONE, unit="Go")

        for attr, val in kwargs.items():
            if val is not None and hasattr(self, f'_ComponentHDD__{attr}'):
                self.__setattr__(attr, val)

    @property
    def capacity(self) -> int:
        if self.__capacity.value is None:
            self.__capacity.value = self.DEFAULT_HDD_CAPACITY
            self.__capacity.status = Status.DEFAULT
        return self.__capacity.value

    @capacity.setter
    def capacity(self, value: int) -> None:
        self.__capacity.value = value

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        impact = self.IMPACT_FACTOR[impact_type]['impact']
        significant_figures = rd.min_significant_figures(impact)
        return impact, significant_figures

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self, model=None) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_pe(self, model=None) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_adp(self, model=None) -> NumberSignificantFigures:
        raise NotImplementedError

    def to_dto(self, original_disk: Disk) -> Disk:
        disk = Disk()
        for attr, val in original_disk.dict().items():
            if hasattr(self, f'_ComponentHDD__{attr}'):
                disk.__setattr__(attr, self.__getattribute__(attr))
            else:
                disk.__setattr__(attr, original_disk.__getattribute__(attr))
        return disk
