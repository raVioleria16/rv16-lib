from pydantic import BaseModel
import httpx
from .utils import get_object_from_config
from .logger import logger

# class ConfigurationManagerResponse(BaseModel):
#     pass

class ConfigurationManagerProxy(BaseModel):
    hostname: str = "srv-configuration-manager"
    port: int = 8000
    register_path: str = "/register-service"
    get_path: str = "/get-service-configuration"

    async def _send_request(self, url: str, payload: dict, timeout: int = 5):
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

    async def register(self, source: str, data: dict):
        payload = {source: data}
        url = f"http://{self.hostname}:{self.port}{self.register_path}"
        response = await self._send_request(url, payload)
        return response

    async def get(self, source: str, target: str):
        payload = {"source": source, "target": target}
        url = f"http://{self.hostname}:{self.port}{self.get_path}"
        response = await self._send_request(url, payload)
        return response

configuration_manager = ConfigurationManagerProxy()
