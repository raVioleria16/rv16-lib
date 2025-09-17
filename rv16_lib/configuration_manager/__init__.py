from typing import TypeVar, Type, Optional
from pydantic import BaseModel
import httpx

from rv16_lib.configuration_manager.entities import ConfigurationPayload
from rv16_lib.configuration_manager.exceptions import ConfigurationManagerProxyException
from rv16_lib.logger import logger


# Create a type variable for the Config model
TConfig = TypeVar("TConfig", bound=BaseModel)

class ConfigurationManagerProxy(BaseModel):
    hostname: str = "srv-configuration-manager"
    port: int = 8000
    register_path: str = "/register-service"
    get_path: str = "/get-service-configuration"

    @staticmethod
    async def _send_request(url: str, payload: dict, timeout: int = 5):
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Sending request to ConfigurationManager at {url}...")
                response = await client.post(url, json=payload, timeout=timeout)
                response.raise_for_status()
                logger.info("Request successful! ✅")
                return response
                # TODO - parse response to ConfigurationManagerResponse
                # return ConfigurationManagerResponse(**response.json())
        except httpx.RequestError as e:
            logger.error(f"Failed to send request: {e} ❌")
            raise e

    async def register(self, service: str, configuration: ConfigurationPayload):
        payload = {
            "service": service,
            "configuration": configuration.model_dump()
        }
        url = f"http://{self.hostname}:{self.port}{self.register_path}"

        response = await self._send_request(url, payload)

        if response.status_code != 200:
            raise ConfigurationManagerProxyException(status_code=response.status_code, message=response.text)

        return response.json()


    async def get(self, source: str, target: str, model_type: Optional[Type[TConfig]] = None):
        payload = {"source": source, "target": target}
        url = f"http://{self.hostname}:{self.port}{self.get_path}"
        response = await self._send_request(url, payload)

        if response.status_code != 200:
            logger.error(f"Failed to send request: {response} <UNK>")

        response = model_type(**response.json()) if model_type else response.json()
        return response

configuration_manager = ConfigurationManagerProxy()
