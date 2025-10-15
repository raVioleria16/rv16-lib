import json
import redis
from typing import Optional, Any, Union

from rv16_lib.exceptions import RV16Exception
from rv16_lib.logger import logger
from rv16_lib.storage.database_connector import DatabaseConnector, DatabaseElement


class RedisElement(DatabaseElement):
    key: str
    value: Union[str, int, float]


class RedisConnector(DatabaseConnector):

    def __init__(self, host: str, port: int, db: int):
        """
        Initializes the Redis client using environment variables for configuration.
        """

        try:
            self.client: redis.Redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            # A simple ping to check for connection
            self.client.ping()
            logger.info("Connected to Redis successfully.")
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise RV16Exception(status_code=500,
                                message=f"Failed to connect to Redis")
        except Exception as e:
            logger.error(f"An unexpected error occurred during Redis connection: {e}")
            raise RV16Exception(status_code=500,
                                message="An unexpected error occurred during Redis connection")


    def insert_one(self, element: RedisElement):
        """
        Inserts a single key-value pair into Redis.
        """
        if not self.client:
            raise RV16Exception(status_code=500,
                                message="Redis client not initialized")

        try:
            self.client.set(element.key, element.value)
            logger.info(f"Successfully inserted key: {element.key}")
            return True

        except (ValueError, TypeError) as e:
            logger.error(f"Error serializing value for key {element.key}: {e}")
            raise RV16Exception(status_code=500,
                                message=f"Error serializing value for key {element.key}")
        except Exception as e:
            logger.error(f"Error inserting key {element.key}: {e}")
            raise RV16Exception(status_code=500,
                                message=f"Error inserting key {element.key}")


    def delete(self, element: RedisElement):
        """
        Deletes a single key-value pair from Redis.
        """
        if not self.client:
            raise RV16Exception(status_code=500,
                                message="Redis client not initialized")

        try:
            self.client.delete(element.key + ":*")
            logger.info(f"Successfully deleted key: {element.key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting key {element.key}: {e}")
            raise RV16Exception(status_code=500,
                                message=f"Error deleting key {element.key}")


    def update(self, element: RedisElement):
        """
        Updates the value of a single key in Redis.
        """
        if not self.client:
            raise RV16Exception(status_code=500,
                                message="Redis client not initialized")

        try:
            self.client.set(element.key, element.value)
            logger.info(f"Successfully updated key: {element.key}")
            return True
        except Exception as e:
            logger.error(f"Error updating key {element.key}: {e}")
            raise RV16Exception(status_code=500,
                                message=f"Error updating key {element.key}")


    async def find(self, element: RedisElement) -> str:
        """
        Finds a single key's value in Redis.
        """
        if not self.client:
            raise RV16Exception(status_code=500,
                                message="Redis client not initialized")

        try:
            value = await self.client.get(element.key)
            if value:
                # Assuming the value is a JSON string
                return value
            else:
                logger.warning(f"Key not found: {element.key}")
                raise RV16Exception(status_code=500,
                                    message=f"Key '{element.key}' not found")
        except Exception as e:
            logger.error(f"Error finding key {element.key}: {e}")
            raise RV16Exception(status_code=500,
                                message=f"Error finding key '{element.key}")

    def execute_query(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Redis does not support arbitrary queries.")