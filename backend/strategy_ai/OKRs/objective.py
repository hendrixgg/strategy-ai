from dataclasses import dataclass
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class Objective(BaseModel):
    name: str = Field()
    id: UUID = Field(default_factory=uuid4)
