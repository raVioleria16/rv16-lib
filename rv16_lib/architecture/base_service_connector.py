from abc import ABC
from typing import TypeVar

from pydantic import BaseModel

from rv16_lib.configuration_manager import configuration_manager as cm, ServiceConfigurationRequest

class BaseConnectionParams(BaseModel):
    hostname: str
    port: int

class BaseServiceConfig(BaseModel):
    provider: str
    name: str

TConnectionParams = TypeVar("TConnectionParams", bound=BaseConnectionParams)
TServiceConfig = TypeVar("TServiceConfig", bound=BaseServiceConfig)

class BaseServiceConnector:

    def __init__(self, config: TServiceConfig):
        self.url = None
        self.connection = None
        self.config = config
        self.provider = self.config.provider
        self.srv_name = self.config.name

    async def setup_connections(self, cm_provider: str, output_type): # TODO - tipizzare
        self.connection = await cm.get(payload=ServiceConfigurationRequest(service=self.srv_name,
                                                                           provider=cm_provider),
                                       output_type=output_type)

    # async def call(self, *args, **kwargs):
    #     raise NotImplementedError("Subclasses must implement this method")