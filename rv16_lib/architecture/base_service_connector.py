# TODO - capire se si può eliminare
# from typing import TypeVar, Optional, Any, Type
#
# from pydantic import BaseModel
#
# class BaseServiceConfig(BaseModel):
#     provider: str
#     hostname: str
#
#
# # TConnectionParams = TypeVar("TConnectionParams", bound=BaseConnectionParams)
# TServiceConfig = TypeVar("TServiceConfig", bound=BaseServiceConfig)
#
#
# class BaseServiceConnector:
#
#     def __init__(self, config: TServiceConfig):
#         self.url = None
#         self.connection: Optional[Any] = None
#         self.config = config
#         self.provider = self.config.provider
#         self.srv_name = self.config.hostname
#
#     # def setup_connections(self, cm_proxy: ConfigurationManagerProxy, cm_provider: str, output_type: Optional[Type]):
#     #     self.connection = cm_proxy.get(payload=CMConfigurationRequest(service=self.srv_name,
#     #                                                                        provider=cm_provider),
#     #                                    output_type=output_type)
