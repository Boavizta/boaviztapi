from fastapi import APIRouter, status, Body
from fastapi.params import Depends

from boaviztapi.model.crud_models.portfolio_model import PortfolioCollection, PortfolioModel
from boaviztapi.model.services.portfolio_service import PortfolioService
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user

portfolio_router = APIRouter(
    prefix='/v1/portfolio',
    tags=['portfolio'],
    dependencies=[Depends(get_current_user)]
)

@portfolio_router.post("/",
                       response_description="Add a new portfolio",
                       response_model=PortfolioModel,
                       status_code=status.HTTP_201_CREATED,
                       response_model_by_alias=False,
                       )
async def create_portfolio(portfolio: PortfolioModel = Body(...), service: PortfolioService = Depends(PortfolioService.get_crud_service)):
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
async def list_portfolios(service: PortfolioService = Depends(PortfolioService.get_crud_service)):
    return await service.get_all()

@portfolio_router.get("/{id}",
                      response_description="Get a single portfolio",
                      response_model=PortfolioModel,
                      response_model_by_alias=False,
                      )
async def find_portfolio(id: str = Depends(validate_id), service: PortfolioService = Depends(PortfolioService.get_crud_service)):
    return await service.get_by_id(id)

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