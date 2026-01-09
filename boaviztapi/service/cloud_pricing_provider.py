import os.path

import pandas as pd

from boaviztapi import data_dir
from boaviztapi.model.cloud_prices.cloud_prices import AzurePriceModel, GcpPriceModel, AWSPriceModel
from boaviztapi.model.crud_models.configuration_model import CloudConfigurationModel


cloud_region_map_path = os.path.join(data_dir, 'electricity/cloud_region_to_electricity_maps.csv')
cloud_region_map = pd.read_csv(cloud_region_map_path, header=0)
def _estimate_cloud_region(localisation: str, provider: str) -> str:
    """
    Estimate the approximate cloud region in which the device is located by using a mapping file. The mapping file
    contains a map between Electricity Maps zones and cloud provider regions.

    Args:
        localisation: str - The country/zone-code in which the cloud configuration is made
        provider: str - cloud provider, e.g. 'aws'

    Returns:
        Nearest cloud provider region to the provided Electricity Maps zone code
    """
    localisation = localisation.upper().strip()
    provider = provider.lower().strip()
    if localisation not in cloud_region_map['zone_code'].unique():
        raise ValueError(f"Given localisation {localisation} is not mapped to any cloud region of provider {provider}!")
    if provider not in cloud_region_map['provider'].unique():
        raise ValueError(f"Given provider {provider} is not recognised!")
    region = cloud_region_map[(cloud_region_map['zone_code'] == localisation)
                              & (cloud_region_map['provider'] == provider)]['region'].values[0]
    if not region:
        raise ValueError(f"No cloud region found for localisation {localisation} and provider {provider}!")
    return region


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

    def _df_to_pydantic(self, df: pd.DataFrame, region: str, instance_id: str, saving: str | None = None) -> list[AWSPriceModel]:
        result = []
        for item in df.to_dict(orient='records'):
            item['region'] = region
            item['id'] = instance_id
            if saving:
                item['saving'] = saving
                result.append(AWSPriceModel.model_validate(item))
                return result
            # No saving specified, use all of them
            for saving in self.savings_types:
                item['saving'] = saving
                result.append(AWSPriceModel.model_validate(item))
        return result

    def get_all(self, region: str, instance_id: str) -> list[AWSPriceModel]:
        region = region.lower().strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid AWS region!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid AWS instance!")
        return self._df_to_pydantic(df=self.aws_prices.xs((region, instance_id), level=('region', 'id')), region=region, instance_id=instance_id)


    def get_prices_with_saving(self, region:str, savings_type: str, instance_id: str) -> list[AWSPriceModel]:
        region = region.lower().strip()
        savings_type = savings_type.strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid AWS region!")
        if savings_type not in self.savings_types:
            raise ValueError(f"Savings type {savings_type} is not a valid AWS savings type! Check for case-sensitivity!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid AWS instance!")
        return self._df_to_pydantic(df=self.aws_prices.xs((region, savings_type, instance_id), level=('region', 'saving', 'id')), region=region, saving=savings_type, instance_id=instance_id)

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

    @classmethod
    def _normalise_instance_id(cls, instance_id: str):
        """
        Normalise archetype instance_id to match the pricing map instance_ids
        e.g. "standard_d32ds_v4" -> "d32dsv4"
        """
        instance_id = instance_id.replace('standard', '')
        instance_id = instance_id.replace('_', '')
        return instance_id.lower().strip()

    def _df_to_pydantic(self, df: pd.DataFrame, region: str, instance_id: str, saving: str | None = None) -> list[
        AzurePriceModel]:
        result = []
        for item in df.to_dict(orient='records'):
            item['region'] = region
            item['id'] = instance_id
            if saving:
                item['saving'] = saving
                result.append(AzurePriceModel.model_validate(item))
                return result
            # No saving specified, use all of them
            for saving in self.savings_types:
                item['saving'] = saving
                result.append(AzurePriceModel.model_validate(item))
        return result

    def get_all(self, region: str, instance_id: str) -> list[AzurePriceModel]:
        region = region.lower().strip()
        instance_id = self._normalise_instance_id(instance_id)
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid Azure region!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid Azure instance!")
        return self._df_to_pydantic(df=self.azure_prices.xs((region, instance_id), level=('region', 'id')), region=region, instance_id=instance_id)

    def get_prices_with_saving(self, region: str, instance_id: str, savings_type: str) -> list[AzurePriceModel]:
        region = region.lower().strip()
        savings_type = savings_type.strip()
        instance_id = self._normalise_instance_id(instance_id)
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid Azure region!")
        if savings_type not in self.savings_types:
            raise ValueError(
                f"Savings type {savings_type} is not a valid Azure savings type! Check for case-sensitivity!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid Azure instance!")
        return self._df_to_pydantic(df=self.azure_prices.xs((region, savings_type, instance_id), level=('region', 'saving', 'id')), region=region, saving=savings_type, instance_id=instance_id)


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

    @staticmethod
    def _df_to_pydantic(df: pd.DataFrame, region: str, instance_id: str) -> GcpPriceModel:
        result = []
        for item in df.to_dict(orient='records'):
            item['region'] = region
            item['id'] = instance_id
            result.append(GcpPriceModel.model_validate(item))
        if len(result) == 0:
            raise ValueError("The returned dictionary from the get_all GCP provider is empty!")
        return result[0]


    def get_all(self, region: str, instance_id: str) -> GcpPriceModel:
        region = region.lower().strip()
        instance_id = instance_id.lower().strip()
        if region not in self.regions:
            raise ValueError(f"Region {region} is not a valid GCP region!")
        if instance_id not in self.instance_ids:
            raise ValueError(f"Instance {instance_id} is not a valid GCP instance!")
        return self._df_to_pydantic(self.gcp_prices.xs((region, instance_id), level=('region', 'id')), region, instance_id)



