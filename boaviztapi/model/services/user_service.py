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
    def get_crud_service(cls) -> GenericPydanticCRUDService[UserModel]:
        return cls()

    def get_mongo_collection(self):
        return self.mongo_collection