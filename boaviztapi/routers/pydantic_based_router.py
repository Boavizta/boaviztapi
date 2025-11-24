import logging
from typing import Any, Mapping, TypeVar, Generic, Type, Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Body, HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.errors import PyMongoError

from boaviztapi.application_context import get_app_context
from boaviztapi.model.crud_models.basemodel import BaseCRUDCollection, BaseCRUDModel

TModel = TypeVar("TModel", bound=BaseCRUDModel)

max_count = 1000

def validate_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

class GenericPydanticCRUDService(Generic[TModel]):
    def __init__(
            self,
            model_class: Type[TModel],
            collection_class: Type[BaseCRUDCollection[TModel]],
            mongo_collection: AsyncCollection[Mapping[str, Any] | Any],
            collection_name: str,
    ):
        self.model_class = model_class
        self.collection_class = collection_class
        self.mongo_collection = mongo_collection
        self.collection_name = collection_name
        self.app_context = get_app_context()
        self._logger = logging.getLogger(collection_name + "_router")

    async def create(self, item: TModel = Body(...)):
        """
        Create a new record in the database.
        """
        new_item = item.model_dump(by_alias=True, exclude={"id"})
        result = await self.mongo_collection.insert_one(new_item)
        new_item["_id"] = result.inserted_id

        return self.model_class(**new_item)

    async def get_all(self) -> BaseCRUDCollection[TModel]:
        """
        List all the record collection data in the database.
        The response is unpaginated and limited to 1000 results.
        """
        return self.collection_class(items = [self.model_class(**item) for item in await self.mongo_collection.find().to_list(max_count)])

    async def get_by_id(self, id: str) -> TModel:
        """
        Get the record for a specific `id`.
        """
        if (
            item := await self.mongo_collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return self.model_class(**item)

        raise HTTPException(status_code=404, detail=f"Item from collection '{self.collection_name}' with id={id} was not found")

    async def get_all_by_filter(
            self,
            filter: Mapping[str, str],
            projection: Optional[Mapping[str, int]] = None,
            options: Optional[Mapping[str, str]] = None
    ) -> BaseCRUDCollection[TModel]:
        try:
            kwargs: dict[str, Any] = {}
            if projection:
                kwargs["projection"] = projection
            if options:
                kwargs["options"] = options
            return self.collection_class(items = await self.mongo_collection.find(filter, **kwargs).to_list(max_count))
        except PyMongoError:
            raise HTTPException(status_code=400, detail="Invalid query filter, cannot return items!")

    async def get_one_by_filter(self, filter: Mapping[str, str], projection: Mapping[str, int] = None, options: Mapping[str, str] = None) -> TModel:
        kwargs: dict[str, Any] = {}
        if projection:
            kwargs["projection"] = projection
        if options:
            kwargs["options"] = options
        if (
            item := await self.mongo_collection.find_one(filter, **kwargs)
        ) is not None:
            return self.model_class(**item)
        self._logger.warning(f"No item was found in the '{self.collection_name}' collection with the specified filter: {filter}.")
        raise HTTPException(status_code=404, detail="No item found with the specified filter!")



    async def update(self, id: str, item: TModel = Body(...)) -> TModel:
        """
        Update individual fields of an existing record.

        Only the provided fields will be updated.
        Any missing or `null` fields will be ignored.
        """
        item = {
            k: v for k, v in item.model_dump(by_alias=True).items() if v is not None and k != '_id'
        }

        if len(item) >= 1:
            update_result = await self.mongo_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": item},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return self.model_class(**update_result)
            else:
                raise HTTPException(status_code=404, detail=f"Item from collection '{self.collection_name}' with id={id} was not found")

        # The update is empty, but we should still return the matching document:
        if (existing_item := await self.mongo_collection.find_one({"_id": ObjectId(id)})) is not None:
            return self.model_class(**existing_item)

        raise HTTPException(status_code=404, detail=f"Item from collection '{self.collection_name}' with id={id} was not found")

    async def delete(self, id: str) -> Response:
        """
        Remove a single record from the database.
        """
        delete_result = await self.mongo_collection.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(status_code=404, detail=f"Item from collection '{self.collection_name}' with id={id} was not found")
