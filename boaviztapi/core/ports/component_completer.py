from abc import ABC, abstractmethod
from typing import Optional


class ComponentCompleter(ABC):
    """Port for completing component specifications from external data sources
    (fuzzy matching, density lookups, consumption profiles).
    """

    @abstractmethod
    def complete_cpu_from_name(self, cpu_name: str) -> Optional[dict]:
        """Fuzzy-match a CPU name against known specs and return matched attributes.

        Returns:
            Dict with keys: name, manufacturer, family, model_range, tdp,
            core_units, threads, die_size, source. Or None if no match.
        """
        ...

    @abstractmethod
    def complete_ram_density(
        self,
        manufacturer: Optional[str] = None,
        process: Optional[float] = None,
    ) -> Optional[dict]:
        """Look up RAM density from manufacturer and process node.

        Returns:
            Dict with keys: density (float), source (str),
            min (float), max (float), manufacturer (str, possibly corrected).
            Or None if no match.
        """
        ...

    @abstractmethod
    def complete_ssd_density(
        self,
        manufacturer: Optional[str] = None,
        layers: Optional[int] = None,
    ) -> Optional[dict]:
        """Look up SSD density from manufacturer and NAND layer count.

        Returns:
            Dict with keys: density (float), source (str),
            min (float), max (float), manufacturer (str, possibly corrected).
            Or None if no match.
        """
        ...

    @abstractmethod
    def get_cpu_consumption_profile(
        self,
        cpu_manufacturer: Optional[str] = None,
        cpu_model_range: Optional[str] = None,
    ) -> Optional[dict]:
        """Look up CPU consumption profile parameters.

        Returns:
            Dict with keys 'a', 'b', 'c', 'd' (model coefficients for
            logarithmic power model), or None if no match.
        """
        ...
