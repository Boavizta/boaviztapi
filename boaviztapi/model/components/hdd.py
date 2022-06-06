import boaviztapi.utils.roundit as rd
from boaviztapi.model.components.component import Component, NumberSignificantFigures
from boaviztapi.dto.components import Disk


class ComponentHDD(Component):

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

        self.__capacity = self.DEFAULT_HDD_CAPACITY

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def capacity(self) -> int:
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        self.__capacity = value

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

    @classmethod
    def from_dto(cls, disk: Disk) -> 'ComponentHDD':
        if disk.type.lower() != cls.__DISK_TYPE:
            raise ValueError(f'wrong disk type, expect `{cls.__DISK_TYPE}`, got `{disk.type}`')
        return cls(**disk.dict())
