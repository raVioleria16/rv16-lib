from pydantic import BaseModel
from starlette import status

from rv16_lib import logger
from rv16_lib.exceptions import RV16Exception
from rv16_lib.architecture.base_provider import BaseProvider
from rv16_lib.configuration_manager import ConfigurationManagerProxy
from rv16_lib.configuration_manager.entities import ServiceRegistrationRequest, ServicePairingRequest

class PairedServiceConfig(BaseModel):
    provider: str
    host: str
    port: int


class BaseService:

    def __init__(self):
        self.service_name = None
        self.providers: dict[str, BaseProvider] = {}

    def register_service(self, cm_proxy: ConfigurationManagerProxy, provider: str, configuration: dict):
        logger.info("Starting service registration...")

        request = ServiceRegistrationRequest(
            provider=provider,
            service=self.service_name,
            configuration=configuration
        )
        response = cm_proxy.register(request)
        logger.info(f"Service registration response: {response}")
        return response

    def initialize_service(self):
        raise NotImplementedError()

    def get_provider(self, provider: str) -> BaseProvider:

        if not self.providers or len(self.providers) == 0:
            raise RV16Exception(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                message="No providers available. Please initialize the service properly."
            )

        p = self.providers.get(provider)
        if not p:
            raise RV16Exception(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                message=f"Provider {provider} not supported."
            )
        return p

