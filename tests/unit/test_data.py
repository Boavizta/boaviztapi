import csv
import os.path

import pytest

from boaviztapi import data_dir_prod
from boaviztapi.service.factor_provider import get_available_countries

# Always use prod data for these tests
cloud_path = os.path.join(data_dir_prod, "archetypes/cloud")
providers_path = os.path.join(data_dir_prod, "archetypes/cloud/providers.csv")
regions_path = os.path.join(data_dir_prod, "archetypes/cloud/regions.csv")
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


def test_region_mapping_providers_exist(providers):
    """Test that all providers in regions.csv exist in providers.csv"""
    if not os.path.exists(regions_path):
        pytest.skip("regions.csv not found")

    with open(regions_path, "r") as f:
        reader = csv.DictReader(f)
        region_providers = set()
        for row in reader:
            provider = row["provider"].strip()
            region_providers.add(provider)
            if provider not in providers:
                pytest.fail(
                    f"Provider '{provider}' in regions.csv not found in providers.csv"
                )


def test_region_mapping_usage_locations_valid():
    """Test that all usage_location codes in regions.csv are valid NATO country codes"""
    if not os.path.exists(regions_path):
        pytest.skip("regions.csv not found")

    # Get valid country codes (reverse=True returns codes, not names)
    valid_countries = get_available_countries(reverse=True)

    with open(regions_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage_location = row["usage_location"].strip()
            provider = row["provider"].strip()
            region = row["region"].strip()

            if usage_location not in valid_countries:
                pytest.fail(
                    f"Usage location '{usage_location}' for {provider}/{region} "
                    f"not found in available countries: {valid_countries}"
                )


def test_region_mapping_uniqueness():
    """Test that each provider-region pair is unique in regions.csv"""
    if not os.path.exists(regions_path):
        pytest.skip("regions.csv not found")

    seen = set()
    with open(regions_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            provider = row["provider"].strip()
            region = row["region"].strip()
            key = (provider, region)

            if key in seen:
                pytest.fail(
                    f"Duplicate provider-region pair found: {provider}/{region}"
                )
            seen.add(key)
