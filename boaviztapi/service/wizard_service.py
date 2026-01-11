import glob
import os

import numpy as np
import pandas as pd
import logging
import json
from datetime import datetime

from boaviztapi.model.crud_models.configuration_model import CloudConfigurationModel, OnPremiseConfigurationModel, \
    CloudServerUsage
from boaviztapi.service.electricity_maps.carbon_intensity_provider import CarbonIntensityProvider
from boaviztapi.service.cloud_pricing_provider import _estimate_localisation, AWSPriceProvider, AzurePriceProvider, \
    GcpPriceProvider

from boaviztapi.service.utils_provider import data_dir

# Initialise logger
log = logging.getLogger(__name__)

# Data directory
cloud_dir = os.path.join(data_dir, 'archetypes/cloud')
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

# Dataframe with pricing availability
pricing_availability = pd.read_csv(os.path.join(data_dir, 'electricity/electricitymaps_zones.csv'),
                                   header=0)

def _cloud_instance_to_cloud_config(input_onprem_config: OnPremiseConfigurationModel, cloud_instance: dict) -> CloudConfigurationModel:
    try:
        cloud_usage_model = CloudServerUsage(
            localisation=input_onprem_config.usage.localisation,
            lifespan=input_onprem_config.usage.lifespan,
            method=input_onprem_config.usage.method,
            serverLoad=input_onprem_config.usage.serverLoad,
            serverLoadAdvanced=input_onprem_config.usage.serverLoadAdvanced
        )
        model = CloudConfigurationModel(
            type='cloud',
            name=input_onprem_config.name + '-lift&shift',
            created=datetime.now(),
            cloud_provider=cloud_instance['provider.name'],
            instance_type=cloud_instance['id'],
            usage=cloud_usage_model,
            user_id=input_onprem_config.user_id,
        )
    except Exception as e:
        raise ValueError(f"Error while converting cloud instance to cloud configuration: {e}") from e
    return model

def _provider_factory(provider: str):
    if provider == 'aws':
        return AWSPriceProvider()
    elif provider == 'azure':
        return AzurePriceProvider()
    elif provider == 'gcp':
        return GcpPriceProvider()
    else:
        raise ValueError(f"Unknown cloud provider: {provider}")


def strategy_lift_shift(input_config: OnPremiseConfigurationModel, provider_name: str) -> CloudConfigurationModel:
    provider_name = provider_name.strip().lower()
    if provider_name not in all_cloud_configs['provider.name'].unique():
        raise ValueError(f"Provider {provider_name} not found in the cloud archetypes")

    # Gather filter parameters
    input_vcpus = input_config.cpu_core_units * input_config.cpu_quantity
    input_ram = input_config.ram_capacity * input_config.ram_quantity

    # Limit the filter parameters to the maximum values available in the cloud archetypes
    provider_configs = all_cloud_configs[all_cloud_configs['provider.name'] == provider_name]
    if input_vcpus > provider_configs['vcpu'].max():
        log.warning(f"input_vcpus[{input_vcpus}] > provider_configs['vcpu'].max()[{provider_configs['vcpu'].max()}]."
                    f"Given on-premise virtual CPU cores requirements exceed the biggest vcpu size available at {provider_name}. "
                    f"Limiting input_vcpus to the maximum provided by the cloud provider!")
        input_vcpus = min(input_vcpus, provider_configs['vcpu'].max())
    if input_ram > provider_configs['memory'].max():
        log.warning(f"input_ram[{input_ram}] > provider_configs['memory'].max()[{provider_configs['memory'].max()}]. "
                    f"Given on-premise memory requirements exceed the biggest memory size available at {provider_name}. "
                    f"Limiting input_ram to the maximum provided by the cloud provider!")
        input_ram = min(input_ram, provider_configs['memory'].max())

    # Make a filter mask for the dataframe
    mask = (
            (all_cloud_configs['provider.name'] == provider_name) &
            (all_cloud_configs['vcpu'] >= input_vcpus) &
            (all_cloud_configs['memory'] >= input_ram)
    )
    # Filter the dataframe with the mask
    filtered_configs = all_cloud_configs[mask].copy()
    # Sort the filtered dataframe by vcpu, memory and ssd_storage
    filtered_configs = filtered_configs.sort_values(
        by=['vcpu', 'memory'],
        ascending=[True, True]
    )
    if len(filtered_configs) == 0:
        raise ValueError(f"No cloud configuration found for provider {provider_name} that fits the given requirements!")
    best_config = filtered_configs.iloc[0].to_dict()
    return _cloud_instance_to_cloud_config(input_config, best_config)

def strategy_right_sizing(input_config: CloudConfigurationModel) -> CloudConfigurationModel:
    return CloudConfigurationModel()

async def strategy_greener_region(input_config: CloudConfigurationModel) -> CloudConfigurationModel:
    if not input_config.usage.localisation:
        raise ValueError("A localisation is required to compute the greener cloud strategy")
    # Gather all the regions for the given provider and instance type

    provider_data = _provider_factory(input_config.cloud_provider)
    regions = provider_data.get_regions_for_instance(input_config.instance_type)

    if len(regions) == 1:
        log.info(
            f"No better configuration option was found for {input_config.cloud_provider}/{input_config.instance_type}")
        return input_config
    # Check the carbon footprint of each region
    locations = []
    for region in regions:
        try:
            locations.append(_estimate_localisation(region, input_config.cloud_provider))
        except Exception as e:
            log.warning(f"Error while computing carbon intensity for {region}: {e}")
            continue
    locations = np.unique(locations)
    intensities = {}
    carbon_intensity_cache = await CarbonIntensityProvider.get_cache_scheduler('monthly').get_results()
    carbon_intensity_cache = {key: (json.loads(value) if isinstance(value, str) else value) 
                                  for key, value in carbon_intensity_cache.items()}
    for location in locations:
        try:
            # FIXME: Remove this filter after demo!
            # Only return regions with prices
            if pricing_availability.loc[pricing_availability['Zone Code'] == location, 'Day-ahead price'].values[0] == 'False':
                continue

            for carbon_intensity in carbon_intensity_cache.values():
                if carbon_intensity['zone'] == location:
                    intensities[location] = carbon_intensity['carbonIntensity']
        except Exception as e:
            log.warning(f"Error while computing carbon intensity for {location}: {e}")
            continue
    if intensities == {}:
        raise ValueError('Could not compute the carbon intensity for any of the regions of the given cloud configuration!')
    greenest_location = min(intensities, key=intensities.get)
    if not greenest_location:
        raise ValueError('Could not compute the greenest location for the given cloud configuration!')

    # If the greenest location is the current one, return the same config
    if greenest_location == input_config.usage.localisation:
        log.info(
            f"No better configuration option was found for {input_config.cloud_provider}/{input_config.instance_type}")
        return input_config

    # Set the new location to the cloud configuration and send it back
    input_config.usage.localisation = greenest_location
    return input_config