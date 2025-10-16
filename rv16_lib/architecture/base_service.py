from starlette import status

from rv16_lib import logger
from rv16_lib.exceptions import RV16Exception
from rv16_lib.architecture.base_provider import BaseProvider
from rv16_lib.configuration_manager import ConfigurationManagerProxy
from rv16_lib.configuration_manager.entities import CMRegistrationRequest


class BaseService:

    def __init__(self):
        self.service_name = None
        self.providers: dict[str, BaseProvider] = {}

    def register_service(self, cm_proxy: ConfigurationManagerProxy, provider: str, configuration: dict):
        logger.info("Starting service registration...")

        request = CMRegistrationRequest(
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
        try:
            return self.providers[provider]
        except Exception:
            raise RV16Exception(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                message=f"Provider {provider} not supported."
            )