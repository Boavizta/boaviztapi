import os
from typing import Optional, Union

import pandas as pd

from boaviztapi import data_dir
from boaviztapi.core.ports.archetype_repository import ArchetypeRepository
from boaviztapi.service.archetype import (
    get_archetype,
    get_cloud_instance_archetype,
    get_cloud_region_mapping,
    get_component_archetype,
    get_device_archetype_lst,
    get_device_archetype_lst_with_type,
    get_iot_device_archetype,
    get_server_archetype,
    get_user_terminal_archetype,
    list_cloud_regions,
)


class CsvArchetypeRepository(ArchetypeRepository):
    """Adapter that reads archetype data from CSV files via the existing service functions."""

    def get_archetype(self, archetype_id: str, csv_path: str) -> Union[dict, bool]:
        return get_archetype(archetype_id, csv_path)

    def get_server_archetype(self, archetype_name: str) -> Union[dict, bool]:
        return get_server_archetype(archetype_name)

    def get_cloud_instance_archetype(
        self, archetype_name: str, provider: str
    ) -> Union[dict, bool]:
        return get_cloud_instance_archetype(archetype_name, provider)

    def get_component_archetype(
        self, archetype_name: str, component_type: str
    ) -> Union[dict, bool]:
        return get_component_archetype(archetype_name, component_type)

    def get_user_terminal_archetype(self, archetype_name: str) -> Union[dict, bool]:
        return get_user_terminal_archetype(archetype_name)

    def get_iot_device_archetype(self, archetype_name: str) -> Union[dict, bool]:
        return get_iot_device_archetype(archetype_name)

    def get_device_archetype_lst(self, path: str) -> list[str]:
        return get_device_archetype_lst(path)

    def get_device_archetype_lst_with_type(self, path: str, name: str) -> list[str]:
        return get_device_archetype_lst_with_type(path, name)

    def get_cloud_region_mapping(self, provider: str, region: str) -> Optional[str]:
        return get_cloud_region_mapping(provider, region)

    def list_cloud_regions(self, provider: Optional[str] = None) -> list[dict]:
        return list_cloud_regions(provider)

    def list_cloud_providers(self) -> list[str]:
        df = pd.read_csv(os.path.join(data_dir, "archetypes/cloud/providers.csv"))
        return df["provider.name"].tolist()
