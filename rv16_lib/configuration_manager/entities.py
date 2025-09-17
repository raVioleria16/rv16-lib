from typing import Optional
from pydantic import BaseModel


class ServiceRequest(BaseModel):
    provider: str

class ServiceRegistrationRequest(ServiceRequest):
    """
    Pydantic model for the request body of the /register-service endpoint.
    This validates the incoming data, ensuring it has a service_name (string)
    and a configuration (dictionary).
    """
    service: str
    configuration: dict

class ServicePairingRequest(ServiceRequest):
    service: str
    target: str
    configuration: dict

class ServiceConfigurationRequest(ServiceRequest):
    service: str
    target: str

