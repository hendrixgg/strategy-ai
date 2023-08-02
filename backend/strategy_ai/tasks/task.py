import uuid
from enum import Enum
import datetime
import json
import pickle
import os
from typing import Iterator, Optional, Callable
from pydantic import BaseModel, Field


class TaskState(Enum):
    PREPARING: str = "preparing"
    READY: str = "ready"
    RUNNING: str = "running"
    FINISHED: str = "finished"


class TaskType(BaseModel):
    name: str = Field(description="The name of the task")
    id: int = Field(description="The id of the task")


class TaskTypeEnum(TaskType, Enum):
    SURFACING: TaskType = TaskType(name="t1_surfacing", id=1)
    ASSESSMENT: TaskType = TaskType(name="t2_assessment", id=2)


class TaskData(BaseModel):
    """Class for keeping track of a task's data"""
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
    task_type: TaskTypeEnum = Field(description="The type of task",
                                    frozen=True)
    progress_info: str = Field(default="",
                               description="Should be what you would print to the console indicating what progress has been made so far, this variable can change over the course of running the task.")
    results_text: str = Field(default="",
                              description="A string for text outputs of the task results. This will typically be in markdown format.")
    files_available: dict = Field(default_factory=dict,
                                  description="A dict representing a folder that contains all the files that were available during the task execution")
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


def task_save(task: TaskData, directory: str):
    """This function will save the results of the task to the given directory.

    Inside the given directory, the save file will contain:
    - the task's detailed results (pickle file ".pkl")
    - the task's run history (csv file ".csv")
    - the readable copy of the results (markdown text file ".md").
        """
    if TaskData.state != TaskState.FINISHED:
        raise Exception(
            "Cannot save the results yet since the task is not finished")

    new_directory = os.path.join(
        directory, f"{task.task_type.name}-{task.task_type.id}")
    os.mkdir(new_directory)

    with open(file=os.path.join(new_directory, "detailedResults.pkl"), mode="wb") as f:
        pickle.dump(task.detailed_results, file=f)

    with open(file=os.path.join(new_directory, "runHistory.csv"), mode="w", newline="\n") as f:
        for time, entry in task.run_history:
            print(f'{time},"{entry}"', file=f)

    with open(file=os.path.join(new_directory, "readableResults.md"), mode="w", newline="\n") as f:
        print(task.results_text, file=f)


def task_update(task: TaskData) -> bool:
    """Updates the task with the current datetime, if the task is not already finished.
    Args:
        task: A task.TaskData instance to be updated.

    Returns: 
        True if the task was updated, False if the task was already finished.

    Raises:
        None.
    """
    if task.state != TaskState.FINISHED:
        task.date_recent = datetime.datetime.now()
        return True
    else:
        return False


def task_generate_results_before(task: TaskData) -> Iterator[dict]:
    """This function will return a generator that will yield the first few dictionaries that can be sent to the frontend.

    Args:
        `task`: a TaskData instance to be referenced.

    Returns:
        A generator that will yield the first few dictionaries that can be sent to the frontend.

    Raises:
        Exception: If the task.state != TaskState.Ready.
    """
    if task.state == TaskState.PREPARING:
        raise Exception(
            f"Not ready to run task {task.task_type.name}, uuid: {task.id}.")
    elif task.state == TaskState.READY:
        task.message = f"Starting task {task.task_type.name}, uuid: {task.id}."
    elif task.state == TaskState.RUNNING:
        raise Exception(
            f"Already running, task {task.task_type.name}, uuid: {task.id}.")
    else:  # FINISHED
        raise Exception(
            f"Already finished, task {task.task_type.name}, uuid: {task.id}.")

    task.state = TaskState.RUNNING
    task.date_start = datetime.datetime.now()
    yield {"type": "message", "body": task.message}


def task_generate_results_processing(task: TaskData, task_results_generator: Callable[[TaskData], Iterator[dict]]) -> Iterator[dict]:
    """This function will update the task as the results are generated and yielded.

    Args:
        `task`: TaskData instance to be referenced. This is the task that is being run.

        `task_results_generator`: A function that takes in a TaskData instance and returns a generator that yields dictionaries that can both be used to update `task` and can be sent to the frontend.

    Returns:
        A generator of dicts which are all the results of the task.

    Raises:
        None.
    """
    for result in task_results_generator(task):
        match result["type"]:
            case "results_text":
                task.results_text += result["body"] + "\n"
            case "progress_info":
                task.progress_info += result["body"] + "\n"
            case "message":
                task.message = result["body"]
        task_update(task)
        yield result


def dict_iter_ndjson_bytes(dict_iter: Iterator[dict]) -> Iterator[bytes]:
    for d in dict_iter:
        yield bytes(json.dumps(d) + "\n", encoding="ascii")
