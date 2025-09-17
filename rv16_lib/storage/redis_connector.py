import os
import json
import redis
from typing import Dict, Optional, Any

from rv16_lib.logger import logger
from rv16_lib.storage.database_connector import DatabaseConnector, DatabaseElement


class RedisElement(DatabaseElement):
    key: str
    value: Optional[Dict[str, Any]] = None

class RedisConnector(DatabaseConnector):

    def __init__(self, host: str, port: int, db: int):
        """
        Initializes the Redis client using environment variables for configuration.
        """

        try:
            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            # A simple ping to check for connection
            self.client.ping()
            logger.info("Connected to Redis successfully.")
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
        except Exception as e:
            logger.error(f"An unexpected error occurred during Redis connection: {e}")
            self.client = None

    def insert_one(self, element: RedisElement):
        self.client.set(element.key, element.value)

    def delete_one(self, element: RedisElement):
        """
        Deletes a single key-value pair from Redis.
        """
        try:
            if self.client and self.client.exists(element.key):
                self.client.delete(element.key)
                logger.info(f"Successfully deleted key: {element.key}")
                return True
            else:
                logger.warning(f"Key not found or client not connected: {element.key}")
                return False
        except Exception as e:
            logger.error(f"Error deleting key {element.key}: {e}")
            return False

    def update_one(self, element: RedisElement):
        """
        Updates the value of a single key in Redis.
        """
        try:
            if self.client:
                self.client.set(element.key, element.value)
                logger.info(f"Successfully updated key: {element.key}")
                return True
            else:
                logger.warning("Redis client not connected.")
                return False
        except Exception as e:
            logger.error(f"Error updating key {element.key}: {e}")
            return False

    def find_one(self, element: RedisElement) -> Optional[Dict[str, Any]]:
        """
        Finds a single key's value in Redis.
        """
        try:
            if self.client:
                value = self.client.get(element.key)
                if value:
                    # Assuming the value is a JSON string
                    return json.loads(value)
                else:
                    logger.warning(f"Key not found: {element.key}")
                    return None
            else:
                logger.warning("Redis client not connected.")
                return None
        except Exception as e:
            logger.error(f"Error finding key {element.key}: {e}")
            return None

    def find_all(self) -> list[Any]:
        raise NotImplementedError

    def execute_query(self, query: Any):
        raise NotImplementedError

