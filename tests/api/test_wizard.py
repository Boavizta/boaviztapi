import glob
import os
from datetime import datetime

import pandas as pd
import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app
from boaviztapi.model.crud_models.configuration_model import OnPremiseConfigurationModel, OnPremiseServerUsage, \
    CloudConfigurationModel
from boaviztapi.service.wizard_service import strategy_lift_shift

# Pytest Configuration
pytest_plugins = ("pytest_asyncio",)

# Pandas dataframe for configuration checking
cloud_dir = os.path.join(os.path.dirname(__file__), "../../boaviztapi/data/archetypes/cloud")
all_files = glob.glob(os.path.join(cloud_dir, '*.csv'))
try:
    all_files.remove(os.path.join(cloud_dir, 'providers.csv'))
except ValueError:
    pass

# Dataframe of all the cloud configurations in the archetype folder
df_list = []
for filename in all_files:
    df = pd.read_csv(filename)

    file_label = os.path.splitext(os.path.basename(filename))[0]
    # Add the provider name (from filename) as a column
    df['provider.name'] = file_label.strip().lower()
    # Convert memory to float due to some rogue string values in there
    df['memory'] = pd.to_numeric(df['memory'], errors='coerce')
    # Convert the values used for filtering to float64
    df = df.astype({'vcpu': 'float64', 'memory': 'float64', 'ssd_storage': 'float64'})
    df_list.append(df)

# The parsed dataframe with all the cloud configurations
all_cloud_configs: pd.DataFrame = pd.concat(df_list, join="outer", axis=0, ignore_index=True, sort=False)

small_tier_onprem_config = OnPremiseConfigurationModel(
    type="on-premise",
    name="R740",
    created=datetime.now(),
    cpu_quantity=1,
    cpu_core_units=12,
    cpu_tdp=120,
    cpu_architecture="SKYLAKE",
    ram_quantity=2,
    ram_capacity=16,
    ram_manufacturer="Micron",
    ssd_quantity=1,
    ssd_capacity=1000,
    ssd_manufacturer="samsung",
    hdd_quantity=1,
    server_type="rack",
    psu_quantity=2,
    user_id="1234567890",
    usage=OnPremiseServerUsage(
        localisation="NL",
        lifespan=43800,
        method="Electricity",
        avgConsumption=100,
        serverLoad=100,
        operatingCosts=700
    )
)

medium_onpremise_config = OnPremiseConfigurationModel(
    type="on-premise",
    name="R740",
    created=datetime.now(),
    cpu_quantity=2,
    cpu_core_units=24,
    cpu_tdp=120,
    cpu_architecture="SKYLAKE",
    ram_quantity=4,
    ram_capacity=32,
    ram_manufacturer="Micron",
    ssd_quantity=1,
    ssd_capacity=1000,
    ssd_manufacturer="samsung",
    hdd_quantity=1,
    server_type="rack",
    psu_quantity=2,
    user_id="1234567890",
    usage=OnPremiseServerUsage(
        localisation="NL",
        lifespan=43800,
        method="Electricity",
        avgConsumption=100,
        serverLoad=100,
        operatingCosts=700
    )
)

large_tier_onprem_config = OnPremiseConfigurationModel(
    type="on-premise",
    name="R740",
    created=datetime.now(),
    cpu_quantity=4,
    cpu_core_units=96,
    cpu_tdp=120,
    cpu_architecture="SKYLAKE",
    ram_quantity=16,
    ram_capacity=64,
    ram_manufacturer="Micron",
    ssd_quantity=10,
    ssd_capacity=1000,
    ssd_manufacturer="samsung",
    hdd_quantity=1,
    server_type="rack",
    psu_quantity=2,
    user_id="1234567890",
    usage=OnPremiseServerUsage(
        localisation="NL",
        lifespan=43800,
        method="Electricity",
        avgConsumption=100,
        serverLoad=100,
        operatingCosts=700
    )
)


def _check_lift_shift(on_prem: OnPremiseConfigurationModel, cloud: CloudConfigurationModel, provider: str):
    assert cloud.cloud_provider == provider

    # get the instance from the dataframe
    instance_row = all_cloud_configs[
        (all_cloud_configs['provider.name'] == provider) &
        (all_cloud_configs['id'] == cloud.instance_type)
        ]
    assert not instance_row.empty, f"Instance {cloud.instance_type} not found in archetypes for {provider}"
    instance = instance_row.iloc[0]

    # calculate on-premise resources
    on_prem_vcpus = on_prem.cpu_quantity * on_prem.cpu_core_units
    on_prem_ram = on_prem.ram_quantity * on_prem.ram_capacity

    # limit the cpu and ram according to the strategy
    provider_configs = all_cloud_configs[all_cloud_configs['provider.name'] == provider]
    max_vcpu = provider_configs['vcpu'].max()
    max_ram = provider_configs['memory'].max()

    req_vcpus = min(on_prem_vcpus, max_vcpu)
    req_ram = min(on_prem_ram, max_ram)

    # check if the instance has enough resources
    assert instance['vcpu'] >= req_vcpus
    assert instance['memory'] >= req_ram

    # check if the instance choice is optimal
    # filter for valid candidates
    candidates = provider_configs[
        (provider_configs['vcpu'] >= req_vcpus) &
        (provider_configs['memory'] >= req_ram)
        ].sort_values(by=['vcpu', 'memory'], ascending=[True, True])

    assert not candidates.empty
    optimal_instance = candidates.iloc[0]

    # We check if the selected instance is the optimal one (first in sorted list)
    assert cloud.instance_type == optimal_instance['id'], \
        f"Selected instance {cloud.instance_type} is not optimal. Expected {optimal_instance['id']}"


def _check_no_possible_solution_lift_shift(on_prem: OnPremiseConfigurationModel, provider: str):
    """
    If the strategy returns an error, check that there is no possible solution for the given provider
    """
    # calculate on-premise resources
    on_prem_vcpus = on_prem.cpu_quantity * on_prem.cpu_core_units
    on_prem_ram = on_prem.ram_quantity * on_prem.ram_capacity

    # limit the cpu and ram according to the strategy
    provider_configs = all_cloud_configs[all_cloud_configs['provider.name'] == provider]
    max_vcpu = provider_configs['vcpu'].max()
    max_ram = provider_configs['memory'].max()

    req_vcpus = min(on_prem_vcpus, max_vcpu)
    req_ram = min(on_prem_ram, max_ram)

    # filter for valid candidates
    candidates = provider_configs[
        (provider_configs['vcpu'] >= req_vcpus) &
        (provider_configs['memory'] >= req_ram)
        ].sort_values(by=['vcpu', 'memory'], ascending=[True, True])
    return candidates.empty


@pytest.mark.asyncio
@pytest.mark.parametrize("on_premise_config",
                         [small_tier_onprem_config, medium_onpremise_config, large_tier_onprem_config])
@pytest.mark.parametrize("provider", ["aws", "azure", "gcp"])
async def test_lift_shift_all_providers(on_premise_config: OnPremiseConfigurationModel, provider: str):
    """
    Test if the given strategy fits the requirements
    on_prem_memory <= cloud_memory
    on_prem_vcpus <= cloud_memory
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/v1/wizard/lift-shift", params={"provider_name": provider},
                                 json=on_premise_config.model_dump(mode='json'))
        if response.status_code == 200:
            result = CloudConfigurationModel(**response.json())
            _check_lift_shift(on_premise_config, result, provider)
        else:
            assert _check_no_possible_solution_lift_shift(on_premise_config, provider), \
                "There was a solution for this provider but the strategy returned none!"


@pytest.mark.asyncio
async def test_incorrect_provider():
    """
    Test if the strategy fails gracefully given an invalid provider
    """
    with pytest.raises(ValueError):
        strategy_lift_shift(small_tier_onprem_config, "invalid")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/v1/wizard/lift-shift", params={"provider_name": "invalid"},
                                 json=small_tier_onprem_config.model_dump(mode='json'))
        assert response.status_code == 400
