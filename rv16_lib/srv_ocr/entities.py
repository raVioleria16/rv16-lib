from pydantic import BaseModel

from rv16_lib.architecture.base_service_request import BaseServiceRequest


class OCRConnection(BaseModel):
    ...

class OCRRequest(BaseServiceRequest):
    ...

class OCRServiceConfig(BaseModel):
    ...