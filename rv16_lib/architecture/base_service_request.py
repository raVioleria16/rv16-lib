from pydantic import BaseModel


class BaseServiceRequestPayload(BaseModel):
    """ Base class for service payload.
    """
    provider: str

class BaseServiceHttpRequest(BaseModel):
    """ Base class for service HTTP requests.
    """
    host: str
    port: int
