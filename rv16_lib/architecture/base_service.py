from starlette import status

from rv16_lib import logger
from rv16_lib.exceptions import RV16Exception
from rv16_lib.architecture.base_provider import BaseProvider
from rv16_lib.configuration_manager import configuration_manager as cm
from rv16_lib.configuration_manager.entities import ServiceRegistrationRequest, ServicePairingRequest


class BaseService:

    def __init__(self):
        self.service_name = None
        self.providers: dict[str, BaseProvider] = {}

    def register_service(self, provider: str, configuration: dict):
        logger.info("Starting service registration...")

        request = ServiceRegistrationRequest(
            provider=provider,
            service=self.service_name,
            configuration=configuration
        )
        response = cm.register(request)
        logger.info(f"Service registration response: {response}")
        return response

    def initialize_service(self):
        raise NotImplementedError()

    def get_provider(self, provider: str) -> BaseProvider:
        try:
            p = self.providers.get(provider)
            if p:
                return p
        except ValueError:
            pass
        raise RV16Exception(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=f"Provider {provider} not supported."
        )
