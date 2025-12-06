from bson import ObjectId
from fastapi import APIRouter, status, Body, HTTPException
from fastapi.params import Depends
from pydantic import TypeAdapter

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.portfolio_model import PortfolioCollection, PortfolioModel, ExtendedPortfolioModel, \
    ExtendedPortfolioWithResultsModel
from boaviztapi.model.services.portfolio_service import PortfolioService
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.sustainability_provider import add_results_to_configuration
from boaviztapi.utils.costs_calculator import CostCalculator

portfolio_router = APIRouter(
    prefix='/v1/portfolio',
    tags=['portfolio'],
    dependencies=[Depends(get_current_user)]
)

def get_scoped_portfolio_service(current_user: UserPublicDTO = Depends(get_current_user)) -> PortfolioService:
    return PortfolioService(user_id=current_user.sub)

@portfolio_router.post("/",
                       response_description="Add a new portfolio",
                       response_model=PortfolioModel,
                       status_code=status.HTTP_201_CREATED,
                       response_model_by_alias=False,
                       )
async def create_portfolio(portfolio: PortfolioModel = Body(...), service: PortfolioService = Depends(get_scoped_portfolio_service)):
    """
    Insert a new portfolio record.

    A unique `id` will be created and provided in the response.
    """
    return await service.create(portfolio)

@portfolio_router.get("/",
                      response_description="List all portfolios",
                      response_model=PortfolioCollection,
                      response_model_by_alias=False,
                      )
async def list_portfolios(service: PortfolioService = Depends(get_scoped_portfolio_service)):
    return await service.get_all()

@portfolio_router.get("/{id}",
                      response_description="Get a single portfolio",
                      response_model=PortfolioModel,
                      response_model_by_alias=False,
                      )
async def find_portfolio(id: str = Depends(validate_id), service: PortfolioService = Depends(get_scoped_portfolio_service)):
    return await service.get_by_id(id)

@portfolio_router.get(
    "/extended/{id}",
    response_description="Get a single portfolio with the configuration objects nested inside",
    response_model=ExtendedPortfolioWithResultsModel,
    response_model_by_alias=False,
)
async def find_extended_portfolio(
    id: str = Depends(validate_id),
    service: PortfolioService = Depends(get_scoped_portfolio_service),
    duration: float | None = None,
):
    if (
        await service.get_mongo_collection().find_one({"_id": ObjectId(id)})
    ) is None:
        raise HTTPException(status_code=404, detail="No item found with the specified filter!")

    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$lookup": {
            "from": "configurations",
            "let": {"config_ids": "$configuration_ids"},
            "pipeline": [
                {"$match": {"$expr": {"$in": [{"$toString": "$_id"}, "$$config_ids"]}}}
            ],
            "as": "configurations"
        }},
    ]

    cursor = await service.get_mongo_collection().aggregate(pipeline)
    portfolio_data = await cursor.to_list(length=1)

    if not portfolio_data:
        raise HTTPException(status_code=404, detail="No item found with the specified filter!")

    portfolio = TypeAdapter(ExtendedPortfolioModel).validate_python(portfolio_data[0])
    configs = portfolio.configurations

    extended_configs = []

    for c in configs:

        extended_c = await add_results_to_configuration(c)
        # Check if duration is given as param, otherwise use standard config lifespan.
        effective_duration = duration if duration is not None else getattr(c.usage, "lifespan", 1)

        calculator = CostCalculator(duration=effective_duration)
        costs = await calculator.configuration_costs(c)

        extended_c.configuration.costs = costs

        extended_configs.append(extended_c)

    return ExtendedPortfolioWithResultsModel(
        configurations=extended_configs,
        **portfolio.model_dump(exclude={"configurations"})
    )


@portfolio_router.put("/{id}",
                      response_description="Update a portfolio",
                      response_model=PortfolioModel,
                      response_model_by_alias=False,
                      )
async def update_portfolio(id: str = Depends(validate_id), portfolio: PortfolioModel = Body(...), service: PortfolioService = Depends(PortfolioService.get_crud_service)):
    return await service.update(id, portfolio)

@portfolio_router.delete("/{id}", response_description="Delete a portfolio")
async def delete_portfolio(id: str = Depends(validate_id), service: PortfolioService = Depends(PortfolioService.get_crud_service)):
    return await service.delete(id)