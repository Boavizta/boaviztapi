from typing import Optional, Dict, Any, List
import logging

from boaviztapi.service.costs_computation import compute_electricity_costs
from boaviztapi.service.sustainability_provider import get_server_impact_on_premise
from boaviztapi.utils.get_vantage import get_vantage_price

logger = logging.getLogger("boaviztapi.main")


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

        elec_costs = compute_electricity_costs(
            server,
            duration=self.duration,
            location=server.usage.localisation
        )

        if not elec_costs.get("avg") or not elec_costs["avg"].get("price"):
            logger.warning(f"No electricity costs available for server {server.id} at location {server.usage.localisation}")
            price_per_mWh = 0.0
            warnings = [f"No electricity costs available for location '{server.usage.localisation}'."]
        else:
            price_per_mWh = elec_costs["avg"]["price"]
            warnings = elec_costs.get("warnings", [])

        impact = await get_server_impact_on_premise(
            server,
            verbose=False,
            costs=False,
            duration=self.duration
        )

        pe_mj = impact["impacts"]["pe"]["use"]["value"]
        energy_costs = self.compute_energy_cost(pe_mj, price_per_mWh) * 24 * 365 * self.duration
        yearly_op_costs = getattr(server.usage, "operatingCosts", 0.0)
        operating_costs = yearly_op_costs * self.duration
        total_cost = energy_costs + operating_costs

        response = {
            "total_cost": total_cost,
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

    async def portfolio_costs(self, servers: List) -> Dict[str, Any]:
        total_cost = 0.0
        total_breakdown = {"operating_costs": 0.0, "energy_costs": 0.0}
        detailed_costs = []
        portfolio_warnings = []

        for server in servers:
            cost_data = await self.configuration_costs(server)
            total_cost += cost_data["total_cost"]
            total_breakdown["operating_costs"] += cost_data["breakdown"].get("operating_costs", 0.0)
            total_breakdown["energy_costs"] += cost_data["breakdown"].get("energy_costs", 0.0)

            warnings = cost_data.get("warnings", [])
            if warnings:
                portfolio_warnings.extend([f"{server.id}: {w}" for w in warnings])

            detailed_costs.append({
                "configuration_id": getattr(server, "id", None),
                "type": getattr(server, "type", None),
                "total_cost": cost_data["total_cost"],
                "breakdown": cost_data["breakdown"],
                **({"warnings": warnings} if warnings else {})
            })

        response = {
            "total_cost": total_cost,
            "breakdown": total_breakdown,
            "details": detailed_costs
        }

        if portfolio_warnings:
            response["warnings"] = portfolio_warnings

        return response