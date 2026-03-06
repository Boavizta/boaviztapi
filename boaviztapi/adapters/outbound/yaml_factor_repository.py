from boaviztapi.core.ports.factor_repository import FactorRepository
from boaviztapi.service.factor_provider import (
    get_available_countries,
    get_electrical_impact_factor,
    get_electrical_min_max,
    get_gpu_impact_factor,
    get_impact_factor,
    get_iot_impact_factor,
)


class YamlFactorRepository(FactorRepository):
    """Adapter that reads impact factors from the YAML-backed factor_provider module."""

    def get_impact_factor(self, item: str, impact_type: str) -> dict:
        return get_impact_factor(item, impact_type)

    def get_gpu_impact_factor(
        self, component: str, phase: str, impact_type: str
    ) -> dict:
        return get_gpu_impact_factor(component, phase, impact_type)

    def get_electrical_impact_factor(
        self, usage_location: str, impact_type: str
    ) -> dict:
        return get_electrical_impact_factor(usage_location, impact_type)

    def get_electrical_min_max(self, impact_type: str, bound: str) -> float:
        return get_electrical_min_max(impact_type, bound)

    def get_iot_impact_factor(
        self, functional_block: str, hsl: str, impact_type: str
    ) -> float:
        return get_iot_impact_factor(functional_block, hsl, impact_type)

    def get_available_countries(self, reverse: bool = False) -> dict:
        return get_available_countries(reverse)
