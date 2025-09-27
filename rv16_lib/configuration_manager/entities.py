from rv16_lib.architecture.base_service_request import BaseServiceRequest

class ServiceRegistrationRequest(BaseServiceRequest):
    """Request for registering a service.
    Args:
        service: The service that is registering
        configuration: The configuration about the service
    """
    service: str
    configuration: dict

class ServicePairingRequest(BaseServiceRequest):
    """Request for pairing a service with a target application/service.
    Args:
        service: The exposed service which target wants to be paired with
        target: The app/service which should be paired with the service
        configuration: The configuration for the service-target pair
    """
    service: str
    target: str
    configuration: dict

class ServiceConfigurationRequest(BaseServiceRequest):
    """Request for configuring a service.
    Args:
        service: The service name
    """
    service: str

