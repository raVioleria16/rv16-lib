from starlette import status

from rv16_lib.exceptions import RV16Exception
from rv16_lib.architecture.base_provider import BaseProvider
from rv16_lib.configuration_manager import configuration_manager as cm
from rv16_lib.configuration_manager.entities import ServiceRegistrationRequest, ServicePairingRequest


class BaseService:

    def __init__(self):
        self.service_name = None
        self.providers: dict[str, BaseProvider] = {}

    async def register_service(self, provider: str, configuration: dict):
        request = ServiceRegistrationRequest(
            provider=provider,
            service=self.service_name,
            configuration=configuration
        )
        response = await cm.register(request)
        return response

    async def pair_to_service(self, provider: str, service: str, configuration: dict):
        request = ServicePairingRequest(
            provider=provider,
            service=service,
            target=self.service_name,
            configuration=configuration
        )
        response = await cm.register(request)
        return response

    async def initialize_service(self):
        raise NotImplementedError()

    def get_provider(self, provider: str) -> BaseProvider:
        try:
            return self.providers.get(provider)
        except ValueError:
            raise RV16Exception(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                message=f"Provider {provider} not supported."
            )
