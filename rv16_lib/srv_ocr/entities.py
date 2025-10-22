from typing import Optional

from rv16_lib.architecture.base_service_request import BaseServiceHttpRequest, BaseServicePayload


class OCRServiceConfig(BaseServiceHttpRequest, BaseServicePayload):
    ocr_path: Optional[str] = "ocr"

class OCRServicePayload(BaseServicePayload):
    ...