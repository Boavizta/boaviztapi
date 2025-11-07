import os
from typing import List, Union, Dict
import pandas as pd
from boaviztapi import data_dir
from boaviztapi.service.archetype import get_device_archetype_lst as _get_device_archetype_lst


def get_cloud_providers():
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/cloud/providers.csv'))
    return df['provider.name'].tolist()

def get_cloud_instance_types(provider: str) -> List[str]:
    if not os.path.exists(data_dir + '/archetypes/cloud/' + provider + '.csv'):
        raise ValueError(f"No available data for this cloud provider ({provider})")
    return _get_device_archetype_lst(os.path.join(data_dir, 'archetypes/cloud/' + provider + '.csv'))

def get_cloud_instance_types_for_all_providers():
    result = dict()
    cloud_providers = get_cloud_providers()
    for provider in cloud_providers:
        result[provider] = get_cloud_instance_types(provider)
    return result