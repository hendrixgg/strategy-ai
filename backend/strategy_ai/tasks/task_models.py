import uuid
from enum import Enum
import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class TaskState(Enum):
    PREPARING: str = "preparing"
    READY: str = "ready"
    RUNNING: str = "running"
    FINISHED: str = "finished"


class TaskType(BaseModel):
    name: str = Field(description="The name of the task")
    id: int = Field(description="The id of the task")


class TaskTypeEnum(Enum):
    SURFACING: TaskType = TaskType(name="t1_surfacing", id=1)
    ASSESSMENT: TaskType = TaskType(name="t2_assessment", id=2)


class TaskData(BaseModel):
    """Class for keeping track of a task's data"""
    # required fields
    task_type: TaskTypeEnum = Field(description="The type of task",
                                    frozen=True)
    files_available: dict = Field(
        description="A dict representing a folder that contains all the files that were available during the task execution")

    # optional/automatic fields
    state: TaskState = Field(default=TaskState.PREPARING,
                             description="The current state of the task")
    message: str = Field(default="",
                         description="The current message of what the task is doing")
    date_start: Optional[datetime.datetime] = Field(default=None,
                                                    description="The date the task was started")
    date_recent: datetime.datetime = Field(default_factory=datetime.datetime.now,
                                           description="The date the task was last updated")
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          description="The unique id of the task")
    progress_info: str = Field(default="",
                               description="Should be what you would print to the console indicating what progress has been made so far, this variable can change over the course of running the task.")
    results_text: str = Field(default="",
                              description="A string for text outputs of the task results. This will typically be in markdown format.")
    run_history: list[tuple[datetime.datetime, dict]] = Field(default_factory=list,
                                                              description="stores each message from the run history of the task")
    detailed_results: dict = Field(default_factory=dict,
                                   description="stores the detailed results of the task, the data structure is task specific")

    class Config:
        json_encoders = {
            datetime.datetime: lambda dt: dt.isoformat(),
            uuid.UUID: lambda u: str(u),
        }
        use_eunm_values = True
        title = "Task Data Model"
