from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class DatabaseElement(BaseModel):
    ...

class DatabaseConnector(ABC):

    @abstractmethod
    def insert_one(self, element: DatabaseElement):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def delete_one(self, element: DatabaseElement):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def update_one(self, element: DatabaseElement):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def find_one(self, element: DatabaseElement) -> DatabaseElement:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def find_all(self) -> list[DatabaseElement]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def execute_query(self, query: Any) -> list[DatabaseElement]:
        raise NotImplementedError("Subclasses must implement this method")