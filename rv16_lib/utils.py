import os
import yaml
from pydantic import BaseModel
from .logger import get_logger
from typing import TypeVar, Type

# Create a type variable for the Config model
TConfig = TypeVar("TConfig", bound=BaseModel)
logger = get_logger("utils")


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
