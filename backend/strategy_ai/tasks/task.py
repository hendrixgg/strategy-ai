import uuid
from enum import Enum
import datetime
import json
import pickle
import os
from typing import Iterator, Optional
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI

from strategy_ai.ai_core.data_sets.vector_store import FAISSVectorStore

from strategy_ai.tasks.t1_surfacing import task1_init, task1_generate_results
from strategy_ai.tasks.t2_assessment import task2_init, task2_generate_results


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


def task_save(task: TaskData, directory: str) -> None:
    """This function will save the results of the task to the given directory.

    Inside the given directory, the a subdirectory will be created and will contain:
    - the task's detailed results (pickle file ".pkl")
    - the task's run history (csv file ".csv")
    - the readable copy of the results (markdown text file ".md").

    Args:
        task: A task.TaskData instance to be saved.

        directory: A string representing the directory to save the results to.

    Returns:
        None

    Raises:
        Exception: If the task is not finished.
    """
    if TaskData.state != TaskState.FINISHED:
        raise Exception(
            "Cannot save the results since the task is not finished")

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


def task_init(task: TaskData, vector_store: FAISSVectorStore, llm: ChatOpenAI) -> None:
    """This function will initialize the task.

    It will call the task specific initialization function depeding on `task.task_type`. 

    The task specific initalizer must set the task state to ready.

    Args:
        `task`: A task.TaskData instance to be initialized.
        `vector_store`: A vector_store.FAISSVectorStore instance to be used for the task.
        `llm`: A llm instance to be used for the task. This should be ChatOpenAI(model="gpt-3.5-turbo-0613") or some model that supports function calling.

    Returns:
        None

    Raises:
        Exception: If the task is not in the preparing state before calling this function.
        Exception: If the task state was changed while running the task specific initalizer.
    """
    if task.state != TaskState.PREPARING:
        raise Exception(
            f"Cannot initialize task {task.task_type.name}, uuid: {task.id}, state: {task.state}. It needs to be in the preparing state.")

    match task.task_type:
        case TaskTypeEnum.SURFACING:
            task1_init(task, vector_store, llm)
        case TaskTypeEnum.ASSESSMENT:
            task2_init(task, vector_store, llm)

    if task.state != TaskState.PREPARING:
        raise Exception(
            f"Task {task.task_type.name}, uuid: {task.id} was changed to \"{task.state}\" while running the task specific initializer.")


def task_generate_results(task: TaskData) -> Iterator[dict]:
    """This function will return a generator that will yield the dictionaries that can be sent to the frontend.

    Tasks should only be run once, and this function should only be called once per task.

    Args:
        `task`: a TaskData instance to be referenced. This is the task that will be run.

    Returns:
        A generator that will yield the dictionaries that can be sent to the frontend.

    Raises:
        Exception: If the task is not in the ready state.
        Exception: If the task was set to Finished when the task specific results were being generated.
    """
    if task.state != TaskState.READY:
        raise Exception(
            f"Task is not ready to run. Current state: {task.state}")

    task.message = f"Starting task {task.task_type.name}, uuid: {task.id}."
    task.state = TaskState.RUNNING
    task.date_start = datetime.datetime.now()
    yield {"type": "message", "body": task.message}

    # this is where the detailed_results are generated
    # perhaps some messages and progress_info results are generated here also
    # you must ensure that after these results are generated, that the task.detailed_results are pickleable (i.e. no lambda functions)
    match task.task_type:
        case TaskTypeEnum.SURFACING:
            yield from task1_generate_results(task)
        case TaskTypeEnum.ASSESSMENT:
            yield from task2_generate_results(task)

    if task.state != TaskState.RUNNING:
        raise Exception(
            f"Task {task.task_type.name} state should not have changed while running, uuid: {task.id}, state: {task.state}.")

    yield {"type": "message", "body": f"Finished task {task.task_type.name}, uuid: {task.id}."}
    yield {"type": "message", "body": f"Task {task.task_type.name}, uuid: {task.id} took {task.date_recent - task.date_start}."}
    task.state = TaskState.FINISHED


def task_generate_results_with_processing(task: TaskData, save_directory: str | None = None) -> Iterator[dict]:
    """This function will update the task as the results are generated and yielded.

    Args:
        `task`: TaskData instance to be referenced. This is the task that is being run.

        `save_directory`: A string representing the directory to save the results to. If None, the results will not be saved.

    Returns:
        A generator of dicts which are all the results of the task.

    Raises:
        Exception: if one of the results generated has the wrong result type.
    """
    for result in task_generate_results(task):
        match result["type"]:
            case "results_text":
                task.results_text += result["body"] + "\n"
            case "progress_info":
                task.progress_info += result["body"] + "\n"
            case "message":
                task.message = result["body"]
            case _:
                Exception(f"Unknown result type: {result['type']}.")
        task.date_recent = datetime.datetime.now()
        task.run_history.append((task.date_recent, result))
        yield result

    if save_directory is not None:
        yield {"type": "message", "body": f"Saving task {task.task_type.name}, uuid: {task.id}."}
        task_save(task, save_directory)
        yield {"type": "message", "body": f"Saved task {task.task_type.name}, uuid: {task.id}."}


def dict_iter_ndjson_bytes(dict_iter: Iterator[dict]) -> Iterator[bytes]:
    """This function will take an iterator over dictionaries, convert each dictionary to a json string, add a newline, and convert to bytes.
    """
    for d in dict_iter:
        yield bytes(json.dumps(d) + "\n", encoding="ascii")
