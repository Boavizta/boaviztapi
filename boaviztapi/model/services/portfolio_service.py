from typing import Optional

from boaviztapi.application_context import get_app_context
from boaviztapi.model.crud_models.portfolio_model import PortfolioModel, PortfolioCollection
from boaviztapi.routers.pydantic_based_router import GenericPydanticCRUDService


class PortfolioService(GenericPydanticCRUDService[PortfolioModel]):
    def __init__(self, user_id: Optional[str] = None):
        ctx = get_app_context()
        if ctx.mongodb_client is None:
            raise RuntimeError("MongoDB is not available!")
        if ctx.database_name is None:
            raise RuntimeError("Database name is not set! Please set it in the environment variables")

        db = ctx.mongodb_client.get_database(ctx.database_name)
        collection = db.get_collection(name="portfolios")

        super().__init__(
            model_class=PortfolioModel,
            collection_class=PortfolioCollection,
            mongo_collection=collection,
            collection_name="portfolios",
            user_id=user_id
        )

    @classmethod
    def get_crud_service(cls) -> GenericPydanticCRUDService[PortfolioModel]:
        return cls()

    def get_mongo_collection(self):
        return self.mongo_collection

    async def delete_many(self, filter: dict) -> int:
        result = await self.mongo_collection.delete_many(filter)
        return result.deleted_count