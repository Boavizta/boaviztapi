from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field

from boaviztapi.model.cloud_prices.cloud_prices import GcpPriceModel, AWSPriceModel, AzurePriceModel
from boaviztapi.model.crud_models.configuration_model import ConfigurationModelWithResults, OnPremiseConfigurationModel, \
    CloudConfigurationModel
from boaviztapi.model.currency.currency_models import Currency
from boaviztapi.service.cloud_pricing_provider import GcpPriceProvider, AWSPriceProvider, AzurePriceProvider, \
    _estimate_cloud_region
from boaviztapi.service.costs_computation import get_electricity_price
from boaviztapi.service.currency_converter import CurrencyConverter
from boaviztapi.service.sustainability_provider import get_server_impact_on_premise
from boaviztapi.utils.get_vantage import get_vantage_price

class Breakdown(BaseModel):
    operating_costs: float
    energy_costs: Optional[float]

class CostBreakdown(BaseModel):
    total_cost: float
    unit: Optional[str]
    currency: Currency
    breakdown: Breakdown
    warnings: Optional[List[str]] = Field(default_factory=list)

class CurrencyConvertedCostBreakdown(BaseModel):
    local: CostBreakdown
    eur: CostBreakdown
    usd: CostBreakdown


async def _convert_cost_breakdown(local_cost_breakdown: CostBreakdown,
                                  target_currency: Currency) -> CostBreakdown:
    # Convert each cost to the target currency
    converted_total_cost = await CurrencyConverter.convert(
        source_currency=local_cost_breakdown.currency.symbol,
        target_currency=target_currency.symbol,
        amount=local_cost_breakdown.total_cost)
    target_operating_costs = await CurrencyConverter.convert(
        source_currency=local_cost_breakdown.currency.symbol,
        target_currency=target_currency.symbol,
        amount=local_cost_breakdown.breakdown.operating_costs
    )
    target_energy_costs = await CurrencyConverter.convert(
        source_currency=local_cost_breakdown.currency.symbol,
        target_currency=target_currency.symbol,
        amount=local_cost_breakdown.breakdown.energy_costs
    )

    # Re-create the cost breakdown in the target currency
    target_breakdown = Breakdown(
        operating_costs=target_operating_costs.value,
        energy_costs=target_energy_costs.value if target_energy_costs else None
    )

    return CostBreakdown(
        total_cost=converted_total_cost.value,
        unit=local_cost_breakdown.unit.replace(local_cost_breakdown.currency.symbol, target_currency.symbol) if local_cost_breakdown.unit else None,
        currency=target_currency,
        breakdown=target_breakdown,
        warnings=local_cost_breakdown.warnings
    )

class CostCalculator:
    def __init__(self, duration: Optional[float] = 1.0):
        self.duration = duration

    @staticmethod
    def compute_energy_cost(primary_energy_MJ: float, price_per_MWh: float) -> float:
        energy_MWh = primary_energy_MJ / 3600  # MJ -> MWh
        return energy_MWh * price_per_MWh

    async def on_premise_costs(self, server) -> CurrencyConvertedCostBreakdown:
        if not hasattr(server, "usage") or not hasattr(server.usage, "localisation"):
            raise ValueError(f"Configuration {server.id} missing usage or localisation info")

        electricity_price_for_location = await get_electricity_price(
            server,
            location=server.usage.localisation
        )
        warnings = []
        if not electricity_price_for_location:
            price_per_mwh = 0.0
            unit = "EUR"
            warnings += [f"No electricity costs available for location '{server.usage.localisation}'."]
        else:
            price_per_mwh = electricity_price_for_location["value"]
            unit = electricity_price_for_location.get("unit", "EUR/MWh")

        consumed_mwh_per_hour = await self.get_avg_power_consumption(server)
        energy_costs = price_per_mwh * consumed_mwh_per_hour * self.duration

        hourly_operating_costs = getattr(server.usage, "operatingCosts", 0.0)
        operating_costs = hourly_operating_costs * self.duration
        total_cost = energy_costs + operating_costs

        _currency = None
        try:
            _currency = CurrencyConverter.get_currency_by_symbol(unit.split("/")[0])
        except ValueError:
            _currency = CurrencyConverter.get_currency_by_symbol("EUR")

        local_costs = CostBreakdown(
            total_cost=total_cost,
            unit=unit,
            currency=_currency,
            breakdown=Breakdown(operating_costs=operating_costs, energy_costs=energy_costs),
            warnings=warnings
        )

        eur_costs = local_costs
        if local_costs.currency.symbol != "EUR":
            eur_costs = await _convert_cost_breakdown(local_cost_breakdown=local_costs,
                                                      target_currency=CurrencyConverter.get_currency_by_symbol("EUR"))
        usd_costs = await _convert_cost_breakdown(local_cost_breakdown=local_costs,
                                                  target_currency=CurrencyConverter.get_currency_by_symbol("USD"))

        return CurrencyConvertedCostBreakdown(local=local_costs, eur=eur_costs, usd=usd_costs)

    async def get_avg_power_consumption(self, server: OnPremiseConfigurationModel) -> float:
        """
        Return the average power consumption of the server in MWh.
        """
        if server.usage.avgConsumption is not None:
            # Convert Wh to MWh
            return server.usage.avgConsumption * (10**-6)

        impact = await get_server_impact_on_premise(
            server,
            verbose=True,
            duration=self.duration
        )
        if avg_wattage := impact["verbose"]["avg_power"]["value"]:
            # Convert W to MWh
            return avg_wattage * (10**-6)
        else:
            # There is no average power consumption available, so we compute it ourselves using the primary energy output
            megajoules_usage = impact["impacts"]["pe"]["use"]["value"]
            mwh_used = megajoules_usage / 3600
            return mwh_used

    async def cloud_costs(self, server) -> CurrencyConvertedCostBreakdown:
        usage = server.usage

        # FIXME: this is now deprecated
        # vantage_cost = get_vantage_price(
        #     cloud_provider=server.cloud_provider,
        #     instance_type=server.instance_type,
        #     instancePricingType=usage.instancePricingType,
        #     region=usage.localisation
        # )

        if 'gcp' == server.cloud_provider.lower():
            price_provider = GcpPriceProvider()
            cloud_region = _estimate_cloud_region(usage.localisation, server.cloud_provider)
            hourly_costs: GcpPriceModel = price_provider.get_all(region=cloud_region, instance_id=server.instance_type)
            if not hourly_costs:
                raise ValueError(f"There is no pricing information for the cloud region {cloud_region} ({usage.localisation}) and instance type {server.instance_type}")
            hourly_cost = hourly_costs.linux_spot_cost
        elif 'aws' == server.cloud_provider.lower():
            price_provider = AWSPriceProvider()
            cloud_region = _estimate_cloud_region(usage.localisation, server.cloud_provider)
            hourly_costs: list[AWSPriceModel] = price_provider.get_prices_with_saving(region=cloud_region, instance_id=server.instance_type, savings_type=usage.reservedPlan)
            if len(hourly_costs) < 1:
                raise ValueError(f"There is no pricing information for the cloud region {cloud_region} ({usage.localisation}) and instance type {server.instance_type}")
            hourly_cost = hourly_costs[0].linux_spot_min_cost
        elif 'azure' == server.cloud_provider.lower():
            price_provider = AzurePriceProvider()
            cloud_region = _estimate_cloud_region(usage.localisation, server.cloud_provider)
            hourly_costs: list[AzurePriceModel] = price_provider.get_prices_with_saving(region=cloud_region, instance_id=server.instance_type, savings_type=usage.reservedPlan)
            if len(hourly_costs) < 1:
                raise ValueError(f"There is no pricing information for the cloud region {cloud_region} ({usage.localisation}) and instance type {server.instance_type}")
            hourly_cost = hourly_costs[0].linux_spot_min_cost
        else:
            raise ValueError(f"Unknown cloud provider: {server.cloud_provider}")


        operating_costs = hourly_cost * self.duration

        local_costs = CostBreakdown(
            total_cost=operating_costs,
            currency=CurrencyConverter.get_currency_by_symbol("EUR"),
            breakdown=Breakdown(operating_costs=operating_costs, energy_costs=None),
            unit=None
        )
        eur_costs = local_costs
        if local_costs.currency.symbol != "EUR":
            eur_costs = await _convert_cost_breakdown(local_cost_breakdown=local_costs, target_currency=CurrencyConverter.get_currency_by_symbol("EUR"))
        usd_costs = await _convert_cost_breakdown(local_cost_breakdown=local_costs, target_currency=CurrencyConverter.get_currency_by_symbol("USD"))

        return CurrencyConvertedCostBreakdown(local=local_costs, eur=eur_costs, usd=usd_costs)

    async def configuration_costs(self, server: ConfigurationModelWithResults) -> CurrencyConvertedCostBreakdown:
        if server.type == "on-premise":
            return await self.on_premise_costs(server)
        elif server.type == "cloud":
            return await self.cloud_costs(server)
        else:
            raise ValueError(f"Unknown configuration type: {server.type}")


    @staticmethod
    def sum_portfolio_costs(cost_items: List[Dict[str, Any]], currency_symbol: str) -> Dict[str, Any]:
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
            "currency": CurrencyConverter.get_currency_by_symbol(currency_symbol),
            "breakdown": breakdown,
            "details": details
        }

        if warnings:
            result["warnings"] = warnings

        return result