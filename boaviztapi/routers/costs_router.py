from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from boaviztapi import config
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.services import configuration_service
from boaviztapi.model.services.configuration_service import ConfigurationService
from fastapi.params import Depends

from boaviztapi.model.services.portfolio_service import PortfolioService
from boaviztapi.routers.electricity_prices_router import get_electricity_price
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.costs_computation import compute_electricity_costs
from boaviztapi.service.sustainability_provider import get_server_impact_on_premise, get_cloud_impact
from bson import ObjectId

from boaviztapi.utils.get_vantage import get_vantage_price

costs_router = APIRouter(
    prefix='/v1/costs',
    tags=['costs']
)

def compute_energy_cost(primary_energy_MJ: float, price_per_MWh: float) -> float:
    energy_MWh = primary_energy_MJ / 3600  # Converts MJ to MWh
    return energy_MWh * price_per_MWh

def get_scoped_configuration_service(current_user: UserPublicDTO = Depends(get_current_user)) -> ConfigurationService:
    return ConfigurationService(user_id=current_user.sub)

def get_scoped_portfolio_service(current_user: UserPublicDTO = Depends(get_current_user)) -> PortfolioService:
    return PortfolioService(user_id=current_user.sub)

@costs_router.get("/on-premise/{id}")
async def get_costs_on_premise(
    configuration_service: ConfigurationService = Depends(get_scoped_configuration_service),
    id: str = Depends(validate_id),
    duration: Optional[float] = config["default_duration"],
):
    server = await configuration_service.get_by_id(id)
    if not server:
        raise HTTPException(404, f"Configuration with id {id} not found")
    if server.type != "on-premise":
        raise HTTPException(400, "Configuration is not on-premise")

    if not hasattr(server, "usage") or not hasattr(server.usage, "localisation"):
        raise HTTPException(400, f"Configuration {id} missing usage or localisation info")

    elec_costs = compute_electricity_costs(
        server,
        duration=duration,
        location=server.usage.localisation
    )

    avg_energy_cost = elec_costs["avg"]["price"]

    yearly_op_costs = getattr(server.usage, "operatingCosts", 0.0)
    operating_costs = yearly_op_costs / 8760 * duration

    total_cost = avg_energy_cost + operating_costs

    return {
        "total_cost": total_cost,
        "breakdown": {
            "operating_costs": operating_costs,
            "energy_costs": avg_energy_cost
        }
    }

# Currently the price from vantage is not scraped.
# Will need to add this later to make sure that all inputs will result in correct costs.
@costs_router.get("/cloud/{id}")
async def get_costs_cloud(
    configuration_service: ConfigurationService = Depends(get_scoped_configuration_service),
    id: str = Depends(validate_id),
    duration: Optional[float] = config["default_duration"],
):
    cloud_instance = await configuration_service.get_by_id(id)
    if not cloud_instance:
        raise HTTPException(404, f"Configuration with id {id} not found")
    if cloud_instance.type != "cloud":
        raise HTTPException(400, "Configuration is not cloud")

    usage = cloud_instance.usage

    # Get Vantage price from CSV
    vantage_cost = get_vantage_price(
        cloud_provider=cloud_instance.cloud_provider,
        instance_type=cloud_instance.instance_type,
        instancePricingType=usage.instancePricingType,
        region=usage.localisation
    )

    # Compute energy costs
    # pe_mj = cloud_instance.results["impacts"]["pe"]["embedded"]["value"]
    # mwh = pe_mj / 3600
    # electricity_price = get_electricity_price(usage["localisation"])
    # energy_costs = mwh * float(electricity_price)

    operating_costs = vantage_cost * duration

    return {
        "total_cost": operating_costs,
        "breakdown": {
            "operating_costs": operating_costs
        }
    }


@costs_router.get("/portfolio/{id}")
async def get_portfolio_costs(
        portfolio_id: str = Depends(validate_id),
        configuration_service: ConfigurationService = Depends(get_scoped_configuration_service),
        portfolio_service: PortfolioService = Depends(get_scoped_portfolio_service),
        duration: Optional[float] = config["default_duration"],
):
    portfolio = await portfolio_service.get_by_id(portfolio_id)
    if not portfolio:
        raise HTTPException(404, f"Portfolio with id {portfolio_id} not found")

    portfolio_id_str = str(portfolio.id)
    configuration_ids = [str(cid) for cid in portfolio.configuration_ids]
    total_cost = 0.0
    total_breakdown = {"operating_costs": 0.0, "energy_costs": 0.0}
    detailed_costs = []

    for config_id in configuration_ids:
        server = await configuration_service.get_by_id(config_id)
        if not server:
            raise HTTPException(404, f"Configuration with id {config_id} not found")

        if server.type == "on-premise":
            if not hasattr(server, "usage") or not hasattr(server.usage, "localisation"):
                raise HTTPException(400, f"Configuration {config_id} missing usage or localisation info")

            elec_costs = compute_electricity_costs(
                server,
                duration=duration,
                location=server.usage.localisation
            )
            avg_energy_cost = elec_costs["avg"]["price"]
            yearly_op_costs = getattr(server.usage, "operatingCosts", 0.0)
            operating_costs = yearly_op_costs / 8760 * duration
            config_total = avg_energy_cost + operating_costs

        elif server.type == "cloud":
            usage = server.usage
            vantage_cost = get_vantage_price(
                cloud_provider=server.cloud_provider,
                instance_type=server.instance_type,
                instancePricingType=usage.instancePricingType,
                region=usage.localisation
            )
            operating_costs = vantage_cost * duration
            avg_energy_cost = 0.0  # Look into in the future.
            config_total = operating_costs

        else:
            raise HTTPException(400, f"Configuration type inapplicable: {server.type}")

        total_cost += config_total
        total_breakdown["operating_costs"] += operating_costs
        total_breakdown["energy_costs"] += avg_energy_cost

        detailed_costs.append({
            "id": config_id,
            "type": server.type,
            "total_cost": config_total,
            "breakdown": {
                "operating_costs": operating_costs,
                "energy_costs": avg_energy_cost
            }
        })

    return {
        "portfolio_id": portfolio_id_str,
        "total_cost": total_cost,
        "breakdown": total_breakdown,
        "details": detailed_costs
    }