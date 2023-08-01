from enum import Enum


class MessageRole(Enum):
    SYSTEM: str = "system"
    HUMAN: str = "user"
    ASSISTANT: str = "assistant"
    FUNCTION: str = "function"

    def __get__(self, instance, owner):
        return self.value
