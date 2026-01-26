import csv
import os.path

import pytest

from boaviztapi import data_dir_prod

# Always use prod data for these tests
cloud_path = os.path.join(data_dir_prod, "archetypes/cloud")
providers_path = os.path.join(data_dir_prod, "archetypes/cloud/providers.csv")
servers_path = os.path.join(data_dir_prod, "archetypes/server.csv")


@pytest.fixture
def providers():
    with open(providers_path, "r") as f:
        reader = csv.DictReader(f)
        return [row["provider.name"] for row in reader]


@pytest.fixture
def valid_platforms():
    with open(servers_path, "r") as f:
        reader = csv.DictReader(f)
        return {row["id"] for row in reader}


def test_platform_exists_in_server_csv(providers, valid_platforms):
    for provider_name in providers:
        provider_csv_path = f"{cloud_path}/{provider_name}.csv"

        try:
            with open(provider_csv_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    platform = row.get("platform", "").strip()
                    if platform not in valid_platforms:
                        pytest.fail(
                            f"Platform '{platform}' for provider '{provider_name}' not found in server.csv"
                        )
        except FileNotFoundError:
            pytest.fail(
                f"CSV file for provider '{provider_name}' not found: {provider_csv_path}"
            )
