import csv
import os.path

import pytest

cloud_path = os.path.join(
    os.path.dirname(__file__), "../../boaviztapi/data/archetypes/cloud/"
)
providers_path = os.path.join(
    os.path.dirname(__file__), "../../boaviztapi/data/archetypes/cloud/providers.csv"
)
servers_patch = os.path.join(
    os.path.dirname(__file__), "../../boaviztapi/data/archetypes/server.csv"
)


@pytest.fixture
def providers():
    with open(providers_path, "r") as f:
        reader = csv.DictReader(f)
        return [row["provider.name"] for row in reader]


@pytest.fixture
def valid_platforms():
    with open(servers_patch, "r") as f:
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
