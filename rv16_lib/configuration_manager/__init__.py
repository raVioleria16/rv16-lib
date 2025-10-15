import json
from typing import TypeVar, Type, Optional, Union
from pydantic import BaseModel

from rv16_lib.exceptions import RV16Exception
from rv16_lib.configuration_manager.entities import ServiceRegistrationRequest, ServiceConfigurationRequest, \
    ServicePairingRequest
from rv16_lib.configuration_manager.exceptions import ConfigurationManagerProxyException
from rv16_lib.logger import logger
from rv16_lib.utils import call_srv_sync, call_srv_async

# Create a type variable for the Config model
TConfig = TypeVar("TConfig", bound=BaseModel)

class ConfigurationManagerProxy:
    """ A proxy client for interacting with the Configuration Manager service.
    This class provides methods to register services and retrieve service configurations
    from a remote Configuration Manager service via HTTP requests.
    """

    def __init__(self, hostname: str = "srv-configuration-manager", port: int = 8000, register_path: str = "/register-service", get_path: str = "/get-service-configuration"):
        self.hostname = hostname
        self.port = port
        self._register_path = register_path
        self._get_path = get_path

    def register(self, request: ServiceRegistrationRequest) -> dict:
        """Register a service with the Configuration Manager.
        Args:
            request (ServiceRegistrationRequest): The service registration request containing
                service details to be registered

        Returns:
            dict: The JSON response from the configuration manager

        Raises:
            ConfigurationManagerProxyException: If the registration fails (non-200 status code)
            httpx.RequestError: If the request fails due to network or other issues
            httpx.HTTPStatusError: If the response status indicates an error
        """
        url = f"http://{self.hostname}:{self.port}{self._register_path}"
        response = call_srv_sync(method="POST",
                                 url=url,
                                 json=request.model_dump())

        if response.status_code != 200:
            raise ConfigurationManagerProxyException(status_code=response.status_code, message=response.text)

        return response.json()


    def get(self, payload: ServiceConfigurationRequest, output_type: Optional[Type[TConfig]] = None) -> Union[dict, TConfig]:
        """Retrieve service configuration from the Configuration Manager.
        Args:
            payload (ServiceConfigurationRequest): The service configuration request containing
                details about the configuration to retrieve
            output_type (Optional[Type[TConfig]], optional): The Pydantic model type to parse
                the response into. If None, returns raw JSON. Defaults to None.

        Returns:
            Union[TConfig, dict]: The configuration data either as the specified model type
                or as a dictionary if no output_type is provided

        Raises:
            httpx.RequestError: If the request fails due to network or other issues
            httpx.HTTPStatusError: If the response status indicates an error
        """
        url = f"http://{self.hostname}:{self.port}{self._get_path}"
        response = call_srv_sync(method="POST",
                                  url=url,
                                  json=payload.model_dump())

        response_payload = response.json()
        if response.status_code != 200:
            logger.error(f"Failed to send request: {response_payload}")
            raise ConfigurationManagerProxyException(status_code=500,
                                message=f"Failed to send request: {response_payload}")

        # response_payload = json.loads(response_payload)
        return output_type(**response_payload) if output_type else response_payload
