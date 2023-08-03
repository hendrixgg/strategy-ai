from enum import Enum


class MessageRole(str, Enum):
    SYSTEM: str = "system"
    HUMAN: str = "user"
    ASSISTANT: str = "assistant"
    FUNCTION: str = "function"
