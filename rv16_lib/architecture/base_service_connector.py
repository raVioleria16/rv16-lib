from typing import TypeVar, Optional, Any

from pydantic import BaseModel

from rv16_lib.configuration_manager import ServiceConfigurationRequest, ConfigurationManagerProxy


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
        self.connection: Optional[Any] = None
        self.config = config
        self.provider = self.config.provider
        self.srv_name = self.config.name

    def setup_connections(self, cm_proxy: ConfigurationManagerProxy, cm_provider: str, output_type):  # TODO - tipizzare
        self.connection = cm_proxy.get(payload=ServiceConfigurationRequest(service=self.srv_name,
                                                                           provider=cm_provider),
                                       output_type=output_type)
