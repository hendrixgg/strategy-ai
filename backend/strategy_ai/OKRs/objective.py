from uuid import uuid4, UUID
from typing import Optional, List, Dict
from enum import Enum

from pydantic import BaseModel, Field


class ObjectiveName(BaseModel):
    """This class represents the name of an objective.
    This class guides the user to provide a concise name for the objective."""

    verb: str = Field(
        default="", description="A single word describing an action. A verb in present tense, not present continous tense, just present tense.")
    outcome: str = Field(
        default="", description="One or 2 words which are the outcome of this objective.")

    def __str__(self):
        return f"{self.verb} {self.outcome}"


class ObjectiveDefinition(BaseModel):
    """This class represents the definition of an objective.
    This class guides the user to provide a concise definition of the objective."""

    what: str = Field(
        default="", description="A single sentence saying WHAT will be the result of achieveing the objective?")
    why: str = Field(
        default="", description="A single sentence saying WHY is this objective important?")

    def __str__(self):
        return f"{self.what} {self.why}"


class ObjectiveRating(Enum):
    """This enum represents the traffic light rating of an objective."""
    NOT_STARTED: str = "not started"
    RED: str = "red"
    YELLOW: str = "yellow"
    GREEN: str = "green"
    ON_HOLD: str = "on hold"


class ObjectiveProgressCalculationMode(Enum):
    """This enum represents the progress mode of an objective."""
    MANUAL: str = "manual"
    AUTOMATIC: str = "automatic"


class Objective(BaseModel):
    """This class represents an objective."""

    id: Optional[UUID] = Field(
        default_factory=uuid4, description="Unique identifier for the objective")
    name: ObjectiveName = Field(
        default_factory=ObjectiveName, description="Name of the objective")
    definition: ObjectiveDefinition = Field(
        default_factory=ObjectiveDefinition, description="Definition should anser these two questions in two sentences: What is the objective working to achieve? Why is the objective important to the business?")

    childItems: Optional[List[UUID]] = Field(
        description="List of child objectives or key results")
    childWeights: Optional[Dict[UUID, float]] = Field(
        description="Weights of child Items. The sum of weights should be 1.0. If the sum of weights is not 1.0, the weights are normalized to sum to 1.0. If the weights are not provided, the weights are calculated automatically based on the number of child items.")

    progressMode: Optional[ObjectiveProgressCalculationMode] = Field(
        ObjectiveProgressCalculationMode.AUTOMATIC, description="Progress mode of the objective, default is automatic. This can be either manual or automatic. If manual, the progress of the objective is set manually by the user. If automatic, the progress of the objective is calculated based on the progress of the child objectives or key results.")

    progress: Optional[float] = Field(
        default=0.0, description="Progress of the objective. The value can range from 0.0 to 1.0. 0.0 means no progress, 1.0 means objective is complete.")

    calculatedObjectiveRating: Optional[ObjectiveRating] = Field(
        default=ObjectiveRating.NOT_STARTED, description="Traffic light rating of the objective. This is calculated based on the progress of the objective.")

    manualObjectiveRating: Optional[ObjectiveRating] = Field(
        default=ObjectiveRating.NOT_STARTED, description="Traffic light rating of the objective. This is set manually by the user")
