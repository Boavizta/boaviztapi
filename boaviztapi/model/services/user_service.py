from fastapi import HTTPException

from boaviztapi.application_context import get_app_context
from boaviztapi.model.crud_models.user_model import UserModel, UserCollection
from boaviztapi.routers.pydantic_based_router import GenericPydanticCRUDService


class UserService(GenericPydanticCRUDService[UserModel]):
    def __init__(self):
        ctx = get_app_context()
        if ctx.mongodb_client is None:
            raise RuntimeError("MongoDB is not available!")
        if ctx.database_name is None:
            raise RuntimeError("Database name is not set! Please set it in the environment variables")

        db = ctx.mongodb_client.get_database(ctx.database_name)
        collection = db.get_collection(name="users")

        super().__init__(
            model_class=UserModel,
            collection_class=UserCollection,
            mongo_collection=collection,
            collection_name="users"
        )

    @classmethod
    def get_crud_service(cls) -> "UserService":
        return cls()

    def get_mongo_collection(self):
        return self.mongo_collection

    async def delete_by_filter(self, filter: dict) -> int:
        result = await self.mongo_collection.delete_one(filter)
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return result.deleted_count