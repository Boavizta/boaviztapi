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
            "minimum": self.minimum,
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
            "unit": self.unit,
            "embedded": self.manufacture.to_dict(),
            "use": self.use.to_dict(),
        }


@dataclass
class AdpImpact(CategoryImpact):
    description: str = "Use of minerals and fossil resources"
    unit: str = "kbSbeq"


@dataclass
class GwpImpact(CategoryImpact):
    description: str = "Total climate change"
    unit: str = "kgCO2eq"


@dataclass
class PeImpact(CategoryImpact):
    description: str = ("Consumption of primary energy",)
    unit: str = "MJ"


@dataclass
class InstanceRequest:
    provider: str
    instance_type: str
    usage: dict

    def to_dict(self):
        return {
            "provider": self.provider,
            "instance_type": self.instance_type,
            "usage": self.usage,
        }

    def to_url(self):
        return f"/v1/cloud/instance?verbose=false&instance_type={self.instance_type}&provider={self.provider}"
