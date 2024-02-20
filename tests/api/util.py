from dataclasses import dataclass
from typing import Optional

END_OF_LIFE_WARNING = ["End of life is not included in the " "calculation"]
UNCERTAINTY_WARNING = [
    "Uncertainty from technical characteristics is "
    "very important. Results should be interpreted "
    "with caution (see min and max values)"
]


@dataclass
class ImpactOutput:
    maximum: float
    minimum: float
    value: float
    warnings: Optional[list[str]] = None

    def to_dict(self) -> dict:
        res = {
            "max": self.maximum,
            "min": self.minimum,
            "value": self.value,
        }

        if self.warnings:
            res["warnings"] = self.warnings

        return res


@dataclass
class CategoryImpact:
    manufacture: ImpactOutput
    use: ImpactOutput

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "embedded": self.manufacture.to_dict(),
            "unit": self.unit,
            "use": self.use.to_dict(),
        }


@dataclass
class AdpImpact(CategoryImpact):
    description: str = "Use of minerals and fossil ressources"
    unit: str = "kgSbeq"


@dataclass
class GwpImpact(CategoryImpact):
    description: str = "Total climate change"
    unit: str = "kgCO2eq"


@dataclass
class PeImpact(CategoryImpact):
    description: str = "Consumption of primary energy"
    unit: str = "MJ"


@dataclass
class InstanceRequest:
    provider: str
    instance_type: str

    usage: dict = None
    duration: int = None

    use_url_params: bool = False

    def to_dict(self) -> dict:
        if self.use_url_params:
            return None

        res = {
            "provider": self.provider,
            "instance_type": self.instance_type,
        }

        if self.usage:
            res["usage"] = self.usage

        return res

    def to_url(self) -> str:
        url = "/v1/cloud/instance?verbose=false"

        if self.use_url_params:
            url = f"{url}&instance_type={self.instance_type}&provider={self.provider}"

        if self.duration:
            url = f"{url}&duration={self.duration}"

        return url
