import os

import numpy as np
import pandas as pd

from tqdm import tqdm
from boaviztapi import data_dir


azure_path = os.path.join(data_dir, 'instances/azure/azure-instances.json')
azure = pd.read_json(azure_path)


all_regions = azure['pricing'].explode().unique()
all_regions = np.sort([i for i in all_regions if isinstance(i, str)])
all_savings_plans = np.sort([
    "yrTerm1Savings.allUpfront",
    "yrTerm1Standard.allUpfront",
    "yrTerm1Standard.hybridbenefit",
    "yrTerm3Savings.allUpfront",
    "yrTerm3Savings.hybridbenefit",
    "yrTerm3Standard.allUpfront",
    "yrTerm3Standard.hybridbenefit"
])
all_instance_ids = np.sort(azure['instance_type'].unique().tolist())

# Build the prices dataframe for an instance
azure_prices_idx = pd.MultiIndex.from_product([all_regions, all_savings_plans, all_instance_ids], names=['region', 'saving', 'id'])
azure_prices = pd.DataFrame(index=azure_prices_idx)
azure_prices.sort_index(inplace=True)



records = []

# Iterate over the dataframe rows directly using itertuples for speed
for row in tqdm(azure.itertuples(index=False), total=len(azure)):
    instance_id = row.instance_type
    pricing = row.pricing

    if not pricing:
        continue

    for region, region_data in pricing.items():
        # Pre-fetch sub-dictionaries to avoid repeated lookups
        linux_data = region_data.get('linux', {})
        windows_data = region_data.get('windows', {})

        # Pre-fetch values that don't depend on saving plan
        l_hybrid = linux_data.get('hybridbenefit')
        l_ondemand = linux_data.get('ondemand')
        l_spot = linux_data.get('spot_min')
        l_reserved_dict = linux_data.get('reserved', {})

        w_hybrid = windows_data.get('hybridbenefit')
        w_ondemand = windows_data.get('ondemand')
        w_spot = windows_data.get('spot_min')
        w_reserved_dict = windows_data.get('reserved', {})

        for saving_plan in all_savings_plans:
            records.append({
                'region': region,
                'saving': saving_plan,
                'id': instance_id,
                'LinuxHybridBenefit': float(l_hybrid) if l_hybrid is not None else None,
                'LinuxOnDemand': float(l_ondemand) if l_ondemand is not None else None,
                'LinuxReservedCost': float(l_reserved_dict.get(saving_plan)) if l_reserved_dict.get(
                    saving_plan) is not None else None,
                'LinuxSpotMinimumCost': float(l_spot) if l_spot is not None else None,
                'WindowsHybridBenefit': float(w_hybrid) if w_hybrid is not None else None,
                'WindowsOnDemandCost': float(w_ondemand) if w_ondemand is not None else None,
                'WindowsReservedCost': float(w_reserved_dict.get(saving_plan)) if w_reserved_dict.get(
                    saving_plan) is not None else None,
                'WindowsSpotMinimumCost': float(w_spot) if w_spot is not None else None,
            })

# Create DataFrame from records
new_prices = pd.DataFrame(records)

if not new_prices.empty:
    new_prices.set_index(['region', 'saving', 'id'], inplace=True)
    # Reindex to match the pre-calculated index (Cartesian product)
    azure_prices = new_prices.reindex(azure_prices_idx)
else:
    azure_prices = pd.DataFrame(index=azure_prices_idx)

azure_prices.sort_index(inplace=True)


if "__main__" == __name__:
    azure_prices.dropna(how='all', inplace=True)
    azure_prices.to_parquet('azure.parquet', engine='fastparquet')