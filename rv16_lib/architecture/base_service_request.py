from pydantic import BaseModel


class BaseServiceRequest(BaseModel):
    """ Base class for service requests.
    """
    provider: str
    host: str
    port: int