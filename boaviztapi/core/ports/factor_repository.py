from abc import ABC, abstractmethod


class FactorRepository(ABC):
    """Port for accessing environmental impact factors (manufacturing, electricity, IoT, GPU)."""

    @abstractmethod
    def get_impact_factor(self, item: str, impact_type: str) -> dict:
        """Get impact factor for a given item and impact type.

        Raises:
            NotImplementedError: If the factor is not available.
        """
        ...

    @abstractmethod
    def get_gpu_impact_factor(
        self, component: str, phase: str, impact_type: str
    ) -> dict:
        """Get GPU-specific impact factor by sub-component, lifecycle phase, and impact type.

        Raises:
            NotImplementedError: If the factor is not available.
        """
        ...

    @abstractmethod
    def get_electrical_impact_factor(
        self, usage_location: str, impact_type: str
    ) -> dict:
        """Get electricity impact factor for a given country code and impact type.

        Raises:
            NotImplementedError: If the factor is not available.
        """
        ...

    @abstractmethod
    def get_electrical_min_max(self, impact_type: str, bound: str) -> float:
        """Get global min or max electrical impact factor for a given impact type.

        Args:
            bound: 'min' or 'max'

        Raises:
            NotImplementedError: If the factor is not available.
        """
        ...

    @abstractmethod
    def get_iot_impact_factor(
        self, functional_block: str, hsl: str, impact_type: str
    ) -> float:
        """Get IoT impact factor (manufacture + eol) for a functional block, HSL level, and impact type.

        Raises:
            NotImplementedError: If the factor is not available.
        """
        ...

    @abstractmethod
    def get_available_countries(self, reverse: bool = False) -> dict:
        """Get mapping of available country codes to names.

        Args:
            reverse: If True, returns name→code mapping instead of code→name.
        """
        ...
