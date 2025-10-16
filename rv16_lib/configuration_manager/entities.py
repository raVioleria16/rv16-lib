from rv16_lib.entities.base_service_request import BaseServiceRequest

class CMRegistrationRequest(BaseServiceRequest):
    """Request for registering a service.
    Args:
        service: The service that is registering
        configuration: The configuration about the service
    """
    service: str
    configuration: dict

class CMConfigurationRequest(BaseServiceRequest):
    """Request for configuring a service.
    Args:
        service: The service name
    """
    service: str

