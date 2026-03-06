from abc import ABC, abstractmethod
from typing import Optional, Union


class ArchetypeRepository(ABC):
    """Port for accessing archetype configuration data (server, cloud, component, terminal, IoT)."""

    @abstractmethod
    def get_archetype(self, archetype_id: str, csv_path: str) -> Union[dict, bool]:
        """Load a single archetype by ID from the given path.

        Returns:
            Parsed archetype dict, or False if not found.
        """
        ...

    @abstractmethod
    def get_server_archetype(self, archetype_name: str) -> Union[dict, bool]:
        """Load a server archetype by name.

        Returns:
            Parsed archetype dict, or False if not found.
        """
        ...

    @abstractmethod
    def get_cloud_instance_archetype(
        self, archetype_name: str, provider: str
    ) -> Union[dict, bool]:
        """Load a cloud instance archetype by name and provider.

        Returns:
            Parsed archetype dict, or False if not found.
        """
        ...

    @abstractmethod
    def get_component_archetype(
        self, archetype_name: str, component_type: str
    ) -> Union[dict, bool]:
        """Load a component archetype by name and component type (cpu, ram, ssd, etc.).

        Returns:
            Parsed archetype dict, or False if not found.
        """
        ...

    @abstractmethod
    def get_user_terminal_archetype(self, archetype_name: str) -> Union[dict, bool]:
        """Load a user terminal archetype by name.

        Returns:
            Parsed archetype dict, or False if not found.
        """
        ...

    @abstractmethod
    def get_iot_device_archetype(self, archetype_name: str) -> Union[dict, bool]:
        """Load an IoT device archetype by name.

        Returns:
            Parsed archetype dict, or False if not found.
        """
        ...

    @abstractmethod
    def get_device_archetype_lst(self, path: str) -> list[str]:
        """List all archetype IDs from the given CSV path."""
        ...

    @abstractmethod
    def get_device_archetype_lst_with_type(self, path: str, name: str) -> list[str]:
        """List archetype IDs filtered by device_type from the given CSV path."""
        ...

    @abstractmethod
    def get_cloud_region_mapping(self, provider: str, region: str) -> Optional[str]:
        """Map a cloud provider region to a NATO usage_location code.

        Returns:
            NATO country code if mapping exists, None otherwise.
        """
        ...

    @abstractmethod
    def list_cloud_regions(self, provider: Optional[str] = None) -> list[dict]:
        """List available cloud regions, optionally filtered by provider.

        Returns:
            List of dicts with 'provider' and 'region' keys.
        """
        ...

    @abstractmethod
    def list_cloud_providers(self) -> list[str]:
        """List all available cloud provider names."""
        ...
