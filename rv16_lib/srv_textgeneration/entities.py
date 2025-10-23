from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel

from rv16_lib.architecture.base_service_request import BaseServiceHttpRequest, BaseServiceRequestPayload


class TextGenerationServiceConfig(BaseServiceHttpRequest, BaseServiceRequestPayload):
    generation_path: Optional[str] = "generate"

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: Role
    content: Any


class TextGenerationServiceParams(BaseModel):
    messages: list[Message]
    model: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    options: Optional[dict] = None

class OpenAITextGenerationServiceParams(TextGenerationServiceParams):
    tools: Optional[list[dict[str, str]]] = None
    reasoning: Optional[bool] = False

class GoogleTextGenerationServiceParams(TextGenerationServiceParams):
    ...

class TextGenerationRequestPayload(BaseServiceRequestPayload):
    params: TextGenerationServiceParams

