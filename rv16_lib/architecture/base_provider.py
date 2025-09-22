from abc import ABC
import enum


class BaseProviderType(str, enum.Enum):
    ...

class BaseProvider(ABC):
    ...