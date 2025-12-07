from bson import ObjectId
from fastapi import APIRouter, status, Body, HTTPException
from fastapi.params import Depends
from pydantic import TypeAdapter

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.configuration_model import ConfigurationModelWithResults
from boaviztapi.model.crud_models.portfolio_model import PortfolioCollection, PortfolioModel, ExtendedPortfolioModel, \
    ExtendedPortfolioWithResultsModel
from boaviztapi.model.services.portfolio_service import PortfolioService
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.sustainability_provider import add_results_to_configuration, compute_portfolio_totals
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
    impacts: bool = False,
    costs: bool = False,
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
    configs = [ConfigurationModelWithResults(results={}, configuration=c) for c in portfolio.configurations]
    totals = {}
    if costs:
        cost_calculator = CostCalculator()

        for wrapper in configs:

            wrapper.results = await add_results_to_configuration(wrapper)

            if duration is not None:
                effective_duration = duration / 8760
            else:
                effective_duration = getattr(wrapper.configuration.usage, "lifespan", 1)

            cost_calculator.duration = effective_duration

            computed_costs = await cost_calculator.configuration_costs(wrapper.configuration)
            wrapper.results["costs"] = computed_costs

        totals["costs"] = cost_calculator.sum_portfolio_costs([w.results["costs"] for w in configs])
    if impacts:
        for wrapper in configs:
            wrapper.results = await add_results_to_configuration(wrapper)
        totals['impacts'] = await compute_portfolio_totals(configs)

    return ExtendedPortfolioWithResultsModel(
        configurations=configs,
        results=totals,
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