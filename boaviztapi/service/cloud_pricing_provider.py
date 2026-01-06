import os.path

import pandas as pd

from boaviztapi import data_dir


class CloudPriceProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.aws_provider = AWSPriceProvider()
        self.azure_provider = AzurePriceProvider()
        self.gcp_provider = GcpPriceProvider()
        self.valid_providers = ['aws', 'azure', 'gcp']

    def get_all(self, provider: str, region: str, instance_id: str):
        provider = provider.lower().strip()
        if provider == 'aws':
            return self.aws_provider.get_all(region, instance_id)
        elif provider == 'azure':
            return self.azure_provider.get_all(region, instance_id)
        elif provider == 'gcp':
            return self.gcp_provider.get_all(region, instance_id)
        else
            raise ValueError(f"Provider {provider} is not a valid cloud provider! Valid providers are {self.valid_providers}")

    def get_prices_with_saving(self, provider: str, region:str, savings_type: str, instance_id: str):
        provider = provider.lower().strip()
        if provider == 'aws':
            return self.aws_provider.get_prices_with_saving(region, savings_type, instance_id)
        elif provider == 'azure':
            return self.azure_provider.get_prices_with_saving(region, savings_type, instance_id)
        elif provider == 'gcp':
            raise ValueError(f"Provider {provider} does not support savings!")
        else:
            raise ValueError(f"Provider {provider} is not a valid cloud provider! Valid providers are {self.valid_providers}")

class AWSPriceProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        aws_path = os.path.join(data_dir, 'utils/aws_pricing/aws.parquet')
        self.aws_prices = pd.read_parquet(aws_path, engine='fastparquet')
        self.aws_prices.sort_index(inplace=True)
        self.regions = self.aws_prices.index.get_level_values('region').unique().tolist()
        self.savings_types = self.aws_prices.index.get_level_values('saving').unique().tolist()
        self.instance_ids = self.aws_prices.index.get_level_values('id').unique().tolist()

    def get_all(self, region: str, instance_id: str) -> pd.DataFrame:
        region = region.lower().strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid AWS region!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid AWS instance!")
        return self.aws_prices.xs((region, instance_id), level=('region', 'id'))


    def get_prices_with_saving(self, region:str, savings_type: str, instance_id: str):
        region = region.lower().strip()
        savings_type = savings_type.strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid AWS region!")
        if savings_type not in self.regions:
            raise ValueError(f"Savings type {savings_type} is not a valid AWS savings type! Check for case-sensitivity!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid AWS instance!")
        return self.aws_prices.xs((region, savings_type, instance_id), level=('region', 'saving', 'id'))


class AzurePriceProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        azure_path = os.path.join(data_dir, 'utils/azure_pricing/azure.parquet')
        self.azure_prices = pd.read_parquet(azure_path, engine='fastparquet')
        self.azure_prices.sort_index(inplace=True)
        self.regions = self.azure_prices.index.get_level_values('region').unique().tolist()
        self.savings_types = self.azure_prices.index.get_level_values('saving').unique().tolist()
        self.instance_ids = self.azure_prices.index.get_level_values('id').unique().tolist()

    def get_all(self, region: str, instance_id: str):
        region = region.lower().strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid Azure region!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid Azure instance!")
        return self.azure_prices.xs((region, instance_id), level=('region', 'id'))

    def get_prices_with_saving(self, region: str, instance_id: str, savings_type: str):
        region = region.lower().strip()
        savings_type = savings_type.strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid Azure region!")
        if savings_type not in self.regions:
            raise ValueError(
                f"Savings type {savings_type} is not a valid Azure savings type! Check for case-sensitivity!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid Azure instance!")
        return self.azure_prices.xs((region, savings_type, instance_id), level=('region', 'saving', 'id'))

class GcpPriceProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        gcp_path = os.path.join(data_dir, 'utils/gcp_pricing/gcp.parquet')
        self.gcp_prices = pd.read_parquet(gcp_path, engine='fastparquet')
        self.gcp_prices.sort_index(inplace=True)
        self.regions = self.gcp_prices.index.get_level_values('region').unique().tolist()
        self.instance_ids = self.gcp_prices.index.get_level_values('id').unique().tolist()

    def get_all(self, region: str, instance_id: str):
        region = region.lower().strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid GCP region!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid GCP instance!")
        return self.gcp_prices.xs((region, instance_id), level=('region', 'id'))

