from typing import Any, Optional

from bson import ObjectId
from pydantic import Field, ConfigDict, model_validator, BaseModel

from rv16_lib.architecture.base_service_request import BaseServiceHttpRequest
from rv16_lib.storage.database_connector import DatabaseElement

class MongoServiceConfig(BaseServiceHttpRequest):
    dbname: str
    collections: list[str]

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
