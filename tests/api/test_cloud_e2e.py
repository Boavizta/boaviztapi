import csv
import os

import pytest
from httpx import ASGITransport, AsyncClient

from boaviztapi import data_dir
from boaviztapi.main import app

from .util import CloudInstanceRequest

cloud_path = os.path.join(data_dir, "archetypes/cloud")

pytest_plugins = ("pytest_asyncio",)


# Generate test cases for all instances, across all providers
def _generate_cloud_provider_urls():
    urls = []
    try:
        with open(f"{cloud_path}/providers.csv", "r") as providers_fh:
            provider_reader = csv.DictReader(providers_fh)
            for provider_row in provider_reader:
                provider_name = provider_row.get("provider.name")
                provider_csv_path = f"{cloud_path}/{provider_name}.csv"
                try:
                    with open(provider_csv_path, "r") as instances_fh:
                        instances_reader = csv.DictReader(instances_fh)
                        for instances_row in instances_reader:
                            instance_id = instances_row.get("id")
                            request = CloudInstanceRequest(
                                provider_name, instance_id, use_url_params=True
                            )

                            print(f"{provider_name} - {instance_id}")

                            urls.append((request.to_url()))

                except FileNotFoundError:
                    pytest.fail(
                        f"CSV file for provider '{provider_name}' not found: {provider_csv_path}"
                    )
    except FileNotFoundError:
        pytest.fail(f"provider file not found : {cloud_path}/providers.csv")
    return urls


def pytest_generate_tests(metafunc):
    if "cloud_provider_url" in metafunc.fixturenames:
        cloud_provider_urls = _generate_cloud_provider_urls()
        metafunc.parametrize("cloud_provider_url", cloud_provider_urls)


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_all_instances(cloud_provider_url):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get(cloud_provider_url)
        assert res.status_code in [200, 201], (
            f"Http error status code {res.status_code}"
        )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_fractional_gpu_instance_reports_gpu_impact():
    """Azure's NVas_v4 family sells fractions of an MI25 (see issue #563)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        embedded = {}
        for instance_type in ("nv4as_v4", "nv8as_v4", "nv16as_v4", "nv32as_v4"):
            url = CloudInstanceRequest(
                "azure", instance_type, use_url_params=True
            ).to_url()
            res = await ac.get(f"{url}&verbose=true")
            assert res.status_code in [200, 201]

            gpu = res.json()["verbose"].get("GPU-1")
            assert gpu is not None, f"{instance_type} reports no GPU at all"
            embedded[instance_type] = gpu["impacts"]["gwp"]["embedded"]["value"]
            assert embedded[instance_type] > 0

        whole_card = embedded["nv32as_v4"]
        for instance_type, fraction in (
            ("nv4as_v4", 0.125),
            ("nv8as_v4", 0.25),
            ("nv16as_v4", 0.5),
        ):
            assert embedded[instance_type] == pytest.approx(
                whole_card * fraction, rel=0.01
            ), f"{instance_type} should get {fraction} of one MI25"
