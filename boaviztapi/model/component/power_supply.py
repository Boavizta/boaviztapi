import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, NumberSignificantFigures
from boaviztapi.dto.component import PowerSupply


class ComponentPowerSupply(Component):
    NAME = "POWER_SUPPLY"

    DEFAULT_POWER_SUPPLY_WEIGHT = 2.99

    IMPACT_FACTOR = {
        'gwp': {
            'impact': 24.30
        },
        'pe': {
            'impact': 352.00
        },
        'adp': {
            'impact': 8.30E-03
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__unit_weight = Boattribute(value=None, status=Status.NONE, unit="Kg")

        for attr, val in kwargs.items():
            if val is not None and hasattr(self, f'_ComponentPowerSupply__{attr}'):
                self.__setattr__(attr, val)

    @property
    def unit_weight(self) -> float:
        if self.__unit_weight.value is None:
            self.__unit_weight.value = self.DEFAULT_POWER_SUPPLY_WEIGHT
            self.__unit_weight.status = Status.DEFAULT
        return self.__unit_weight.value

    @unit_weight.setter
    def unit_weight(self, value: float) -> None:
        self.__unit_weight.value = value

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        power_supply_impact = self.IMPACT_FACTOR[impact_type]['impact']
        impact = self.__compute_impact_manufacture(power_supply_impact)
        sign_figures = rd.min_significant_figures(power_supply_impact)
        return impact, sign_figures

    def __compute_impact_manufacture(self, power_supply_impact: float) -> float:
        return self.unit_weight * power_supply_impact

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

    def to_dto(self, original_power_supply: PowerSupply) -> PowerSupply:
        power_supply = PowerSupply()
        for attr, val in original_power_supply.dict().items():
            if hasattr(self, f'_ComponentPowerSupply__{attr}'):
                power_supply.__setattr__(attr, self.__getattribute__(attr))
            else:
                power_supply.__setattr__(attr, original_power_supply.__getattribute__(attr))
        return power_supply
