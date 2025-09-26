from abc import ABC
from typing import TypeVar

from pydantic import BaseModel

from rv16_lib.configuration_manager import configuration_manager as cm, ServiceConfigurationRequest

class BaseConnectionParams(BaseModel):
    hostname: str
    port: int

class BaseServiceConfig(BaseModel):
    provider: str

TConnectionParams = TypeVar("TConnectionParams", bound=BaseConnectionParams)
TServiceConfig = TypeVar("TServiceConfig", bound=BaseServiceConfig)

class BaseServiceConnector(ABC):

    def __init__(self, srv_name: str, config: TServiceConfig):
        self.url = None
        self.connection = None
        self.srv_name = srv_name
        self.config = config

    async def setup_connections(self, model_type, provider="local"):
        self.connection = await cm.get(payload=ServiceConfigurationRequest(service=self.srv_name, provider=provider),
                                       model_type=model_type)
        self.url = f"http://{self.connection.hostname}:{self.connection.port}"

    async def call(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")