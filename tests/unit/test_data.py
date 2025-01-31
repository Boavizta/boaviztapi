import csv
import os.path

import pytest

cloud_instance_folder =  os.path.join(os.path.dirname(__file__), "../../boaviztapi/data/archetypes/cloud_instance")
cloud_platform_folder =  os.path.join(os.path.dirname(__file__), "../../boaviztapi/data/archetypes/cloud_platform")
providers_path = os.path.join(os.path.dirname(__file__),"../../boaviztapi/data/archetypes/cloud_instance/providers.csv")
servers_patch = os.path.join(os.path.dirname(__file__),"../../boaviztapi/data/archetypes/server.csv")

@pytest.fixture
def providers():
    with open(providers_path, 'r') as f:
        reader = csv.DictReader(f)
        return [row['provider.name'] for row in reader]

@pytest.fixture
def valid_servers():
    with open(servers_patch, 'r') as f:
        reader = csv.DictReader(f)
        return {row['id'] for row in reader}
    
@pytest.fixture
def valid_platforms(providers):
    results = []
    for provider_name in providers:
        provider_csv_path = f"{cloud_platform_folder}/{provider_name}.csv"
        with open(provider_csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row['id'])
    return results


def test_platform_exists_in_server_csv(providers, valid_servers):
    for provider_name in providers:
        provider_csv_path = f"{cloud_instance_folder}/{provider_name}.csv"

        try:
            with open(provider_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    platform = row.get('platform', '').strip()
                    if platform not in valid_servers:
                        pytest.fail(f"Platform '{platform}' for provider '{provider_name}' not found in server.csv")
        except FileNotFoundError:
            pytest.fail(f"CSV file for provider '{provider_name}' not found: {provider_csv_path}")

def test_instance_exists_in_platform_csv(providers, valid_platforms):
    for provider_name in providers:
        provider_csv_path = f"{cloud_instance_folder}/{provider_name}.csv"

        try:
            with open(provider_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    platform = row.get('platform', '').strip()
                    if platform not in valid_platforms:
                        pytest.fail(f"Platform '{platform}' for provider '{provider_name}' not found in platforms csv files")
        except FileNotFoundError:
            pytest.fail(f"CSV file for provider '{provider_name}' not found: {provider_csv_path}")