import os
from typing import TypeVar, Type, Optional

import httpx
import yaml
from httpx import Response
from pydantic import BaseModel

from rv16_lib.logger import get_logger

# Create a type variable for the Config model
TConfig = TypeVar("TConfig", bound=BaseModel)
logger = get_logger("utils")


async def call_srv(method: str, url: str, payload: Optional[dict] = None, timeout: int = 5) -> Response:
    """ Send an asynchronous HTTP POST request to the specified URL.
   Args:
       method (str): The HTTP method to use (e.g., 'POST', 'GET')
       url (str): The target URL for the request
       payload (dict): The JSON payload to send in the request body
       timeout (int, optional): Request timeout in seconds. Defaults to 5.

   Returns:
       httpx.Response: The HTTP response object

   Raises:
       httpx.RequestError: If the request fails due to network or other issues
       httpx.HTTPStatusError: If the response status indicates an error (raised by raise_for_status())
   """
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Sending request to {url}...")
            response = await client.request(method=method, url=url, json=payload, timeout=timeout)
            response.raise_for_status()
            logger.info("Request successful! ✅")
            return response
    except httpx.RequestError as e:
        logger.error(f"Failed to send request: {e} ❌")
        raise e


def get_object_from_config(config_model: Type[TConfig], filename: str = "app.yaml") -> TConfig:
    """
    Loads a YAML configuration file from the specified path and returns it as a Pydantic object.

    Args:
        filename (str): The name of the configuration file.
        config_model (Type[Config]): The Pydantic model to validate the configuration against.

    Returns:
        Config: An instance of the Pydantic model populated with the configuration data.
    """
    filepath = os.path.join(os.getenv("CONFIG_DIR", "config"), filename)

    logger.info(f"Loading configuration from {filepath}")

    try:
        with open(filepath, 'r') as file:
            config_dict = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {filepath}")
        raise

    # Use the Pydantic model to validate and parse the dictionary
    try:
        result = config_model(**config_dict)
    except Exception as e:
        logger.error(f"Failed to validate configuration from {filepath}: {e}")
        raise

    logger.info("Configuration loaded successfully.")
    return result
