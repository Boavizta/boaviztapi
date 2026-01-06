import glob
import os

import numpy as np
import pandas as pd

from tqdm import tqdm
from boaviztapi import data_dir

aws_path = os.path.join(data_dir, 'instances/aws/instances.json')
aws_paths = glob.glob(os.path.join(data_dir, 'instances/aws/*.json'))
dfs = [pd.read_json(df) for df in aws_paths]
aws = pd.concat(dfs, ignore_index=True)


all_regions = aws['regions'].apply(lambda d: list(d.keys())).explode().unique()
all_regions = np.sort([i for i in all_regions if isinstance(i, str)])
all_savings_plans= np.sort([
    "yrTerm1Convertible.allUpfront",
    "yrTerm1Convertible.noUpfront",
    "yrTerm1Convertible.partialUpfront",
    "yrTerm1Standard.allUpfront",
    "yrTerm1Standard.noUpfront",
    "yrTerm1Standard.partialUpfront",
    "yrTerm3Convertible.allUpfront",
    "yrTerm3Convertible.noUpfront",
    "yrTerm3Convertible.partialUpfront",
    "yrTerm3Standard.allUpfront",
    "yrTerm3Standard.noUpfront",
    "yrTerm3Standard.partialUpfront"
])
all_instance_ids = np.sort(aws['instance_type'].unique().tolist())

# Build the prices dataframe for an instance
aws_prices_idx = pd.MultiIndex.from_product([all_regions, all_savings_plans, all_instance_ids], names=['region', 'saving', 'id'])
aws_prices = pd.DataFrame(index=aws_prices_idx)
aws_prices.sort_index(inplace=True)

pricing_types = ['LinuxOnDemandCost', 'LinuxReservedCost', 'LinuxSpotMinimumCost', 'WindowsOnDemandCost', 'WindowsReservedCost', 'WindowsSpotMinimumCost']
# df.loc[('region', 'savingplan', 'instanceid'), 'column'] = 0.42
def _get_data(data: dict, keys: list[str]) -> float | None:
    try:
        while len(keys) > 0:
            data = data[keys.pop(0)]
        return float(data)
    except Exception:
        pass

def parse_one_instance(instance_id: str) -> None:
    instance = aws[aws['instance_type'] == instance_id]
    if instance.empty:
        raise ValueError(f"Instance {instance_id} not found")
    instance_pricing = instance['pricing'].iloc[0]
    if not instance_pricing:
        raise ValueError(f"No pricing found for instance {instance_id}")
    for region, data in instance_pricing.items():
        for saving_plan in all_savings_plans:
            aws_prices.loc[(region, saving_plan, instance_id), 'OnDemand'] = _get_data(data, ['linux', 'ondemand'])
            aws_prices.loc[(region, saving_plan, instance_id), 'LinuxReservedCost'] = _get_data(data, ['linux', 'reserved', saving_plan])
            aws_prices.loc[(region, saving_plan, instance_id), 'LinuxSpotMinimumCost'] = _get_data(data, ['linux', 'spot_min'])
            aws_prices.loc[(region, saving_plan, instance_id), 'WindowsOnDemandCost'] = _get_data(data, ['mswin', 'ondemand'])
            aws_prices.loc[(region, saving_plan, instance_id), 'WindowsReservedCost'] = _get_data(data, ['mswin', 'reserved', saving_plan])
            aws_prices.loc[(region, saving_plan, instance_id), 'WindowsSpotMinimumCost'] = _get_data(data, ['mswin', 'spot_min'])

for instance_id in tqdm(iterable=aws['instance_type'].unique(), total=len(aws['instance_type'].unique())):
    try:
        parse_one_instance(instance_id)
    except ValueError as e:
        print(f"Error parsing instance {instance_id}: {e}")
        print(f"Skipping...")
        pass


if "__main__" == __name__:
    aws_prices.dropna(how='all', inplace=True)
    aws_prices.to_parquet('aws.parquet', engine='fastparquet')