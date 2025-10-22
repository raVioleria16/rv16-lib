from typing import Optional, Any, Union

from rv16_lib.storage.database_connector import DatabaseConnector, DatabaseElement

class RedisElement(DatabaseElement):
    key: str
    value: Union[str, int, float]
