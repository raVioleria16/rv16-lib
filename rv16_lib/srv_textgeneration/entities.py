from enum import Enum
from typing import Optional

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
    content: str


class TextGenerationServiceParams(BaseModel):
    messages: list[Message]
    system_prompt: str
    user_prompt: str
    model: str
    max_tokens: int
    temperature: float
    optional: Optional[dict] = None

class OpenAITextGenerationServiceParams(TextGenerationServiceParams):
    ...

class GoogleTextGenerationServiceParams(TextGenerationServiceParams):
    ...

class TextGenerationRequestPayload(BaseServiceRequestPayload):
    params: TextGenerationServiceParams

