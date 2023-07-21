from abc import ABC, abstractmethod
from uuid import uuid4
from enum import Enum
from dataclasses import dataclass, asdict
import datetime
import json

from strategy_ai.tasks.path_to_json import path_to_dict


class AutoConvertEnum(Enum):
    def __get__(self, instance, owner):
        return self.value


class TaskStatus(AutoConvertEnum):
    PREPARING: str = "preparing"
    READY: str = "ready"
    RUNNING: str = "running"
    FINISHED: str = "finished"


@dataclass
class TaskResponse():
    """Class for keeping track of the task api responses"""
    status: TaskStatus
    message: str
    date: str
    task_uuid: str
    task_type_id: int
    task_name: str
    # Should be what you would print to the console indicating what progress has been made so far, this variable can change over the course of running the task.
    progress_info: str
    # Depends on the type of task, could be a string for text outputs, an of object for a file, etc. This variable may change over the course of running the task.
    results: str
    # folder indicating all the files that were available during the task execution
    files_available: dict
    # properties about the task being run, such as the parameters chosen to run the task, the date the task was run, etc.
    metadata: dict

    def update(self):
        self.date = str(datetime.datetime.now())


class BaseTask(ABC):
    def __init__(self, task_type: int, task_name: str, availableDataFolder: str):
        """must provide the task type and name.
        you also need to implement the generate_results method
        which is an iterator that will output the results of 
        running the task as it progresses"""
        self.currentResponse = TaskResponse(
            status=TaskStatus.PREPARING,
            message="",
            date="",
            task_uuid=str(uuid4()),
            task_type_id=task_type,
            task_name=task_name,
            progress_info="",
            results="",
            files_available=path_to_dict(availableDataFolder),
            metadata=dict(),
        )

    @abstractmethod
    def generate_results(self):
        if self.currentResponse.status == TaskStatus.PREPARING:
            raise Exception(
                f"Not ready to run task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}.")
        elif self.currentResponse.status == TaskStatus.READY:
            self.currentResponse.message = f"Starting task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}."
        elif self.currentResponse.status == TaskStatus.RUNNING:
            raise Exception(
                f"Already running, task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}.")
        else:  # FINISHED
            raise Exception(
                f"Already finished, task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}.")

        self.currentResponse.status = TaskStatus.RUNNING
        yield self.currentResponse

    def generate_results_json_bytes(self):
        for result in self.generate_results():
            result.update()
            jsonString = json.dumps(asdict(result))
            yield bytes(jsonString, encoding="ascii")
