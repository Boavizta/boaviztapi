from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from boaviztapi import config
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.services import configuration_service
from boaviztapi.model.services.configuration_service import ConfigurationService
from fastapi.params import Depends

from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.costs_computation import compute_electricity_costs
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

    elec_costs = compute_electricity_costs(
        server,
        duration=duration,
        location=server.usage.localisation
    )

    avg_energy_cost = elec_costs["avg"]["price"]

    yearly_op_costs = getattr(server.usage, "operatingCosts", 0.0)
    days = duration or 365
    operating_costs = yearly_op_costs / 365 * days

    total_cost = avg_energy_cost + operating_costs

    return {
        "total_cost": total_cost,
        "breakdown": {
            "operating_costs": operating_costs,
            "energy_costs": avg_energy_cost
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

    elec_costs = compute_electricity_costs(
        cloud_instance,
        duration=duration,
        location=cloud_instance.usage.localisation
    )

    avg_energy_cost = elec_costs["avg"]["price"]

    # Cloud total yearly cost from Vantage
    yearly_total_cost = getattr(cloud_instance, "vantage_total_cost", 0.0)

    days = duration or 365

    total_cloud_cost = yearly_total_cost / 365 * days

    operating_costs = total_cloud_cost - avg_energy_cost

    return {
        "total_cost": total_cloud_cost,
        "breakdown": {
            "operating_costs": operating_costs,
            "energy_costs": avg_energy_cost
        }
    }