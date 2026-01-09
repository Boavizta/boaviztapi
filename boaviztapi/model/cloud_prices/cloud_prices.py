import re
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, BeforeValidator


class AzurePriceModel(BaseModel):
    id: str
    region: str
    saving: str
    linux_on_demand_cost: float | None = Field(None, alias="LinuxOnDemand")
    linux_reserved_cost: float | None = Field(None, alias="LinuxReservedCost")
    linux_spot_min_cost: float | None = Field(None, alias="LinuxSpotMinimumCost")
    linux_hybrid_benefit: float | None = Field(None, alias="LinuxHybridBenefit")
    windows_on_demand_cost: float | None = Field(None, alias="WindowsOnDemandCost")
    windows_reserved_cost: float | None = Field(None, alias="WindowsReservedCost")
    windows_spot_min_cost: float | None = Field(None, alias="WindowsSpotMinimumCost")
    windows_hybrid_benefit: float | None = Field(None, alias="WindowsHybridBenefit")
    model_config = ConfigDict(
        validate_by_alias=True,
    )


def extract_numeric(v: any) -> any:
    if isinstance(v, str):
        # This regex finds the first sequence of digits and decimals
        match = re.search(r"[-+]?\d*\.\d+|\d+", v)
        if match:
            return match.group()
    return v


NumericFloat = Annotated[float, BeforeValidator(extract_numeric)]

class GcpPriceModel(BaseModel):
    id: str
    region: str
    instance_name: str = Field(alias='Instance Name')
    instance_memory: str = Field(alias='Instance Memory')
    vcpus: int = Field(alias="vCPUs")
    linux_on_demand_cost: NumericFloat | None = Field(None, alias="Linux On Demand cost")
    linux_spot_cost: NumericFloat | None = Field(None, alias="Linux Spot cost")
    windows_on_demand_cost: NumericFloat | None = Field(None, alias="Windows On Demand cost")
    windows_spot_cost: NumericFloat | None = Field(None, alias="Windows Spot cost")
    model_config = ConfigDict(
        validate_by_alias=True,
    )

class AWSPriceModel(BaseModel):
    id: str
    region: str
    saving: str
    linux_on_demand_cost: float | None = Field(None, alias="OnDemand")
    linux_reserved_cost: float | None = Field(None, alias="LinuxReservedCost")
    linux_spot_min_cost: float | None = Field(None, alias="LinuxSpotMinimumCost")
    windows_on_demand_cost: float | None = Field(None, alias="WindowsOnDemandCost")
    windows_reserved_cost: float | None = Field(None, alias="WindowsReservedCost")
    windows_spot_min_cost: float | None = Field(None, alias="WindowsSpotMinimumCost")
    model_config = ConfigDict(
        validate_by_alias=True,
    )
