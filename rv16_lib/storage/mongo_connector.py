from typing import Any, Optional, Type, TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pymongo import MongoClient

from rv16_lib import logger
from rv16_lib.storage.database_connector import DatabaseConnector, DatabaseElement, TConfig


class MongoElement(DatabaseElement):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: Optional[ObjectId] = Field(alias="_id", default=None)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.id:
            data["id"] = str(self.id)
        return data

    @model_validator(mode='before')
    def preprocess_id(cls, data: Any):
        if isinstance(data, dict):
            if 'id' in data and isinstance(data["id"], str):
                data['_id'] = ObjectId(data["id"])
        return data

class MongoConnector(DatabaseConnector):

    def __init__(self, host: str, port: int, db_name: str):
        self.client = MongoClient(f'mongodb://{host}:{port}/')
        self.db = self.client[db_name]

        self.db.command('ping')
        logger.info("Connected to MongoDB successfully.")

    def insert_one(self, element: MongoElement, collection_name: str = None) -> ObjectId:
        if not collection_name:
            raise ValueError("Collection name must be provided for MongoDB insert operation.")

        collection = self.db[collection_name]
        result = collection.insert_one(element.model_dump())
        return result.inserted_id


    def insert_many(self, elements: list[MongoElement], collection_name: str = None) -> list[ObjectId]:
        if not collection_name:
            raise ValueError("Collection name must be provided for MongoDB insert operation.")

        collection = self.db[collection_name]
        docs = [element.model_dump() for element in elements]
        result = collection.insert_many(docs)
        return result.inserted_ids


    def delete(self, query: dict, collection_name: str = None) -> int:
        if not collection_name:
            raise ValueError("Collection name must be provided for MongoDB insert operation.")

        collection = self.db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count


    def update(self, query: dict, element: MongoElement, collection_name: str = None) -> int:
        if not collection_name:
            raise ValueError("Collection name must be provided for MongoDB insert operation.")

        collection = self.db[collection_name]

        data = {"$set": element.model_dump()}
        result = collection.update_many(query, data)
        return result.modified_count


    def find(self, query: dict, collection_name: str = None, model_type: Optional[Type[MongoElement]] = None) -> list[MongoElement]:
        if not collection_name:
            raise ValueError("Collection name must be provided for MongoDB insert operation.")

        result = self.db[collection_name].find(query)
        if not result:
            return []

        return [model_type(**r) for r in result] if model_type else list(result)

    def execute_query(self,  query: Any, model_type: Optional[Type[MongoElement]] = None) -> list[MongoElement]:
        pass