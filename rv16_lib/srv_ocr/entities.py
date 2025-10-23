from typing import Optional

from pydantic import BaseModel

from rv16_lib.architecture.base_service_request import BaseServiceHttpRequest, BaseServicePayload


class OCRServiceConfig(BaseServiceHttpRequest, BaseServicePayload):
    ocr_path: Optional[str] = "ocr"

class OCRServicePayload(BaseServicePayload):
    ...

class OCRServiceParams(BaseModel):
    file_bytes: bytes
    content_type: str

class LocalOCRServiceParams(OCRServiceParams):
    ...