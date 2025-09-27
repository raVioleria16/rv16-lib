from typing import Literal

from pydantic import Field

from rv16_lib.architecture.base_service_connector import BaseConnectionParams
from rv16_lib.architecture.base_service_request import BaseServiceRequest


class OCRConnection(BaseConnectionParams):
    ...

class OCRRequest(BaseServiceRequest):
    ...