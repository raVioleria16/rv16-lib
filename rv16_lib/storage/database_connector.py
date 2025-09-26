from abc import ABC, abstractmethod
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel


class DatabaseElement(BaseModel):
    ...

TConfig = TypeVar("TConfig", bound=DatabaseElement)

class DatabaseConnector(ABC):
    # ...
    @abstractmethod
    def insert_one(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def delete(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def find(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def execute_query(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement this method")