from typing import Optional, Dict, Any, List

from boaviztapi.service.costs_computation import compute_electricity_costs
from boaviztapi.service.sustainability_provider import get_server_impact_on_premise
from boaviztapi.utils.get_vantage import get_vantage_price


class CostCalculator:
    def __init__(self, duration: Optional[float] = 1.0):
        self.duration = duration

    @staticmethod
    def compute_energy_cost(primary_energy_MJ: float, price_per_MWh: float) -> float:
        energy_MWh = primary_energy_MJ / 3600  # MJ -> MWh
        return energy_MWh * price_per_MWh

    async def on_premise_costs(self, server) -> Dict[str, Any]:
        if not hasattr(server, "usage") or not hasattr(server.usage, "localisation"):
            raise ValueError(f"Configuration {server.id} missing usage or localisation info")

        elec_costs = await compute_electricity_costs(
            server,
            duration=self.duration,
            location=server.usage.localisation
        )
        avg_block = elec_costs.get("avg") if isinstance(elec_costs, dict) else None
        if not avg_block or "price" not in avg_block:
            price_per_mwh = 0.0
            unit = "EUR" # Needs to be fixed later once we get actual currency or convert to euro.
            warnings = [f"No electricity costs available for location '{server.usage.localisation}'."]
        else:
            price_per_mwh = avg_block["price"]
            unit = avg_block.get("unit", "EUR")
            warnings = elec_costs.get("warnings", [])

        impact = await get_server_impact_on_premise(
            server,
            verbose=False,
            duration=self.duration
        )

        pe_mj = impact["impacts"]["pe"]["use"]["value"]
        energy_costs = self.compute_energy_cost(pe_mj, price_per_mwh) * 24 * 365 * self.duration
        yearly_op_costs = getattr(server.usage, "operatingCosts", 0.0)
        operating_costs = yearly_op_costs * self.duration
        total_cost = energy_costs + operating_costs

        response = {
            "total_cost": total_cost,
            "unit": unit,
            "breakdown": {
                "operating_costs": operating_costs,
                "energy_costs": energy_costs
            }
        }
        if warnings:
            response["warnings"] = warnings

        return response

    def cloud_costs(self, server) -> Dict[str, Any]:
        usage = server.usage

        vantage_cost = get_vantage_price(
            cloud_provider=server.cloud_provider,
            instance_type=server.instance_type,
            instancePricingType=usage.instancePricingType,
            region=usage.localisation
        )

        operating_costs = vantage_cost * self.duration * 24 * 365

        return {
            "total_cost": operating_costs,
            "unit": "EUR",
            "breakdown": {
                "operating_costs": operating_costs
            }
        }

    async def configuration_costs(self, server) -> Dict[str, Any]:
        if server.type == "on-premise":
            return await self.on_premise_costs(server)
        elif server.type == "cloud":
            return self.cloud_costs(server)
        else:
            raise ValueError(f"Unknown configuration type: {server.type}")

    @staticmethod
    def sum_portfolio_costs(cost_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_cost = 0.0
        breakdown = {"operating_costs": 0.0, "energy_costs": 0.0}
        warnings: List[str] = []
        details: List[Dict[str, Any]] = []

        for item in cost_items:
            total_cost += item["total_cost"]
            breakdown["operating_costs"] += item["breakdown"].get("operating_costs", 0.0)
            breakdown["energy_costs"] += item["breakdown"].get("energy_costs", 0.0)

            if "warnings" in item:
                warnings.extend(item["warnings"])

            details.append(item)

        result = {
            "total_cost": total_cost,
            "breakdown": breakdown,
            "details": details
        }

        if warnings:
            result["warnings"] = warnings

        return result