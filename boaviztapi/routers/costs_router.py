from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from boaviztapi import config
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.services.configuration_service import ConfigurationService
from fastapi.params import Depends

from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.sustainability_provider import get_server_impact_on_premise, get_cloud_impact

costs_router = APIRouter(
    prefix='/v1/costs',
    tags=['costs']
)

def compute_energy_cost(primary_energy_MJ: float, price_per_MWh: float) -> float:
    energy_MWh = primary_energy_MJ / 3600  # Converts MJ to MWh
    return energy_MWh * price_per_MWh

def get_scoped_configuration_service(current_user: UserPublicDTO = Depends(get_current_user)) -> ConfigurationService:
    return ConfigurationService(user_id=current_user.sub)

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

    sustainability = await get_server_impact_on_premise(
        server,
        costs=True,
        duration=duration,
        criteria=["pe"]
    )

    try:
        primary_energy_MJ = sustainability.get("impacts", {}).get("pe", {}).get("use", {}).get("value", 0.0)
        price_per_MWh = sustainability.get("costs", {}).get("avg", {}).get("price", 0.0)
    except Exception as e:
        raise HTTPException(500, f"Failed to extract cost info: {e}")

    energy_costs = compute_energy_cost(primary_energy_MJ, price_per_MWh)
    operating_costs = getattr(server.usage, "operatingCosts", 0.0) if server.usage else 0.0
    if duration:
        days = duration
    else:
        days = 365
    operating_costs_per_day = operating_costs / 365
    operating_costs_computed = operating_costs_per_day * days
    total_cost = operating_costs_computed + energy_costs

    return {
        "total_cost": total_cost,
        "breakdown": {
            "operating_costs": operating_costs_computed,
            "energy_costs": energy_costs
        }
    }

@costs_router.get("/cloud/{id}")
async def get_costs_cloud(
        configuration_service: ConfigurationService = Depends(get_scoped_configuration_service),
        id: str = Depends(validate_id),
        duration: Optional[float] = config["default_duration"]
):
    cloud_instance = await configuration_service.get_by_id(id)
    if not cloud_instance:
        raise HTTPException(404, f"Configuration with id {id} not found")
    if cloud_instance.type != "cloud":
        raise HTTPException(400, "Configuration is not cloud")

    sustainability = await get_cloud_impact(
        cloud_instance,
        duration=duration,
        criteria=["pe"]
    )

    primary_energy_MJ = sustainability.get("impacts", {}).get("pe", {}).get("use", {}).get("value", 0.0)
    price_per_MWh = sustainability.get("costs", {}).get("avg", {}).get("price", 0.0)

    energy_costs = compute_energy_cost(primary_energy_MJ, price_per_MWh)
    if duration:
        days = duration
    else:
        days = 365
    total_cost_yearly = getattr(cloud_instance, "vantage_total_cost", 0.0)
    total_cost_computed = total_cost_yearly / 365 * days
    operating_costs_computed = total_cost_computed - energy_costs

    return {
        "total_cost": total_cost_computed,
        "breakdown": {
            "operating_costs": operating_costs_computed,
            "energy_costs": energy_costs
        }
    }