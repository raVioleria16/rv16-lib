import os
from typing import TypeVar, Type, Optional, Union
from pydantic import BaseModel

from rv16_lib.configuration_manager.entities import ServiceRegistrationRequest, ServiceConfigurationRequest, \
    ServicePairingRequest
from rv16_lib.configuration_manager.exceptions import ConfigurationManagerProxyException
from rv16_lib.logger import logger
from rv16_lib.utils import call_srv, get_object_from_config

# Create a type variable for the Config model
TConfig = TypeVar("TConfig", bound=BaseModel)

class ConfigurationManagerProxy:
    """ A proxy client for interacting with the Configuration Manager service.
    This class provides methods to register services and retrieve service configurations
    from a remote Configuration Manager service via HTTP requests.
    """

    def __init__(self, hostname: str = "srv-configuration-manager", port: int = 8000, pair_path: str = "/pair-service", get_path: str = "/get-service-configuration"):
        self.hostname = hostname
        self.port = port
        self.pair_path = pair_path
        self.get_path = get_path

    async def register(self, request: ServiceRegistrationRequest, path: str = "/register-service") -> dict:
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
        url = f"http://{self.hostname}:{self.port}{path}"
        response = await call_srv(method="POST", url=url, payload=request.model_dump())

        if response.status_code != 200:
            raise ConfigurationManagerProxyException(status_code=response.status_code, message=response.text)

        return response.json()

    async def pair(self, request: ServicePairingRequest) -> dict:
        """Pair a service to a target (srv or app) through the Configuration Manager.
        Args:
            request (ServicePairingRequest): The service pairing request containing
                details about the services to be paired

        Returns:
            dict: The JSON response from the configuration manager

        Raises:
            ConfigurationManagerProxyException: If the pairing fails (non-200 status code)
            httpx.RequestError: If the request fails due to network or other issues
            httpx.HTTPStatusError: If the response status indicates an error
        """
        url = f"http://{self.hostname}:{self.port}{self.pair_path}"
        response = await call_srv(url, request.model_dump())

        if response.status_code != 200:
            raise ConfigurationManagerProxyException(status_code=response.status_code, message=response.text)

        return response.json()

    async def get(self, payload: ServiceConfigurationRequest, model_type: Optional[Type[TConfig]] = None) -> Union[dict, TConfig]:
        """Retrieve service configuration from the Configuration Manager.
        Args:
            payload (ServiceConfigurationRequest): The service configuration request containing
                details about the configuration to retrieve
            model_type (Optional[Type[TConfig]], optional): The Pydantic model type to parse
                the response into. If None, returns raw JSON. Defaults to None.

        Returns:
            Union[TConfig, dict]: The configuration data either as the specified model type
                or as a dictionary if no model_type is provided

        Raises:
            httpx.RequestError: If the request fails due to network or other issues
            httpx.HTTPStatusError: If the response status indicates an error
        """
        url = f"http://{self.hostname}:{self.port}{self.get_path}"
        response = await call_srv(url, payload.model_dump())

        if response.status_code != 200:
            logger.error(f"Failed to send request: {response} <UNK>")

        response = model_type(**response.json()) if model_type else response.json()
        return response

configuration_manager = ConfigurationManagerProxy()
