import os
from typing import TypeVar, Type

import httpx
import requests # type: ignore
import yaml # type: ignore
from httpx import Response
from pydantic import BaseModel
from starlette import status

from rv16_lib.exceptions import RV16Exception
from rv16_lib.logger import get_logger

# Create a type variable for the Config model
TConfig = TypeVar("TConfig", bound=BaseModel)
logger = get_logger("utils")

async def call_srv_async(method: str, url: str, **kwargs) -> Response:
    """ Send an asynchronous HTTP POST request to the specified URL.
   Args:
       method (str): The HTTP method to use (e.g., 'POST', 'GET')
       url (str): The target URL for the request
       data (dict, optional): The data to send in the request body. Defaults to None.
       files (dict, optional): Files to send with the request. Defaults to None.
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
            response = await client.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            logger.info("Request successful! ✅")
            return response
    except httpx.RequestError as e:
        logger.error(f"Failed to send request: {e} ❌")
        raise RV16Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Failed to send request to {url}: {e}"
        )
    except Exception as e:
        logger.error(f"Failed to send request: {e} ❌")
        raise RV16Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"An unexpected error occurred: {e}"
        )


def call_srv_sync(method: str, url: str, **kwargs) -> Response:
    """ Send a synchronous HTTP request to the specified URL using the requests library.

   Args:
       method (str): The HTTP method to use (e.g., 'POST', 'GET', 'PUT', 'DELETE')
       url (str): The target URL for the request
       data (dict, optional): The data to send in the request body. Defaults to None.
       files (dict, optional): Files to send with the request (for multipart/form-data). Defaults to None.
       timeout (int, optional): Request timeout in seconds. Defaults to 5.

   Returns:
       requests.Response: The HTTP response object

   Raises:
       requests.exceptions.RequestException: If the request fails due to network, timeout, or other issues.
       requests.exceptions.HTTPError: If the response status indicates an error (raised by raise_for_status()).
   """
    try:
        logger.info(f"Sending request to {url}...")

        # Use requests.request for a generic method call
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )

        # raise_for_status checks for bad status codes (4xx or 5xx)
        logger.info("Request successful! ✅")
        return response

    # Catching the base exception for requests errors, which includes
    # ConnectionError, Timeout, TooManyRedirects, and HTTPError
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send request: {e} ❌")
        raise RV16Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Failed to send request to {url}: {e}"
        )
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.error(f"An unexpected error occurred: {e} ❌")
        raise RV16Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"An unexpected error occurred: {e}"
        )

def get_object_from_config(config_model: Type[TConfig], filename: str = "app.yaml", abs_path: bool = False) -> TConfig:
    """
    Loads a YAML configuration file from the specified path and returns it as a Pydantic object.

    Args:
        filename (str): The name of the configuration file.
        config_model (Type[Config]): The Pydantic model to validate the configuration against.
        abs_path: If True, the filename is treated as an absolute path. Defaults to False.

    Returns:
        Config: An instance of the Pydantic model populated with the configuration data.
    """
    if not abs_path:
        filepath = os.path.join(os.getenv("CONFIG_DIR", "config"), filename)
    else:
        filepath = filename

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
