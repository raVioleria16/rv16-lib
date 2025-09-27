from typing import Literal

from pydantic import Field

from rv16_lib.architecture.base_service_connector import BaseConnectionParams
from rv16_lib.architecture.base_service_request import BaseServiceRequest


class OCRConnection(BaseConnectionParams):
    ...

class OCRRequest(BaseServiceRequest):
    file_content: bytes = Field(..., description="Raw bytes content of the file")
    content_type: str = Literal["image/png", "image/jpeg", "application/pdf"]