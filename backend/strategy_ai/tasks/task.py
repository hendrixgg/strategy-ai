from abc import ABC, abstractmethod
from uuid import uuid4
from enum import Enum
from dataclasses import dataclass, asdict
import datetime
import json
import pickle
import os
import asyncio

from strategy_ai.tasks.path_to_json import path_to_dict


class AutoConvertEnum(Enum):
    def __get__(self, instance, owner):
        return self.value


class TaskStatus(AutoConvertEnum):
    PREPARING: str = "preparing"
    READY: str = "ready"
    RUNNING: str = "running"
    FINISHED: str = "finished"


def iter_over_async(ait, loop):
    """This function will take an async iterator and return a sync iterator that will iterate over the async iterator."""
    ait = ait.__aiter__()

    async def get_next():
        try:
            obj = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None
    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield obj


def sync_generator(asyncGen, asyncEventLoop=asyncio.get_event_loop()):
    """This function will take an async generator and return a sync generator that will iterate over the async generator."""
    return iter_over_async(asyncGen, asyncEventLoop)


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
            date=str(datetime.datetime.now()),
            task_uuid=str(uuid4()),
            task_type_id=task_type,
            task_name=task_name,
            progress_info="",
            results="",
            files_available=path_to_dict(availableDataFolder, ""),
            metadata=dict(),
        )
        self.runHistory: list[dict] = []
        self.detailedResults = {}

    @abstractmethod
    def generate_results(self):
        """This function will return a generator that will yield json strings that can be sent to the frontend."""
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
        yield {"type": "message", "body": self.currentResponse.message}

    def generate_results_json_bytes(self, asyncEventLoop=None, saveDirectory: str | None = None):
        """This function will return a generator that will yield json strings that can be sent to the frontend.
        """
        if asyncEventLoop is None:
            try:
                asyncEventLoop = asyncio.get_event_loop()
            except RuntimeError:
                asyncEventLoop = asyncio.new_event_loop()
        for result in sync_generator(self.generate_results(saveDirectory), asyncEventLoop):
            self.runHistory.append((datetime.datetime.now(), result))
            match result["type"]:
                case "results_text":
                    self.currentResponse.results += result["body"] + "\n"
                case "progress_info":
                    self.currentResponse.progress_info += result["body"] + "\n"
                case "message":
                    self.currentResponse.message = result["body"]
            self.currentResponse.update()
            jsonString = json.dumps(result) + "\n"
            yield bytes(jsonString, encoding="ascii")

    def save(self, directory: str):
        """This function will save the results of the task to the given directory.
            Inside the given directory, the save file will contain:
            - the task's detailed results (pickle file ".pkl")
            - the task's run history (csv file ".csv")
            - the readable copy of the results (markdown text file ".md").
         """
        if self.currentResponse.status != TaskStatus.FINISHED:
            raise Exception(
                "Cannot save the results yet since the task is not finished")

        new_directory = os.path.join(
            directory, f"{self.currentResponse.task_name}-{self.currentResponse.task_uuid}")
        os.mkdir(new_directory)

        with open(file=os.path.join(new_directory, "detailedResults.pkl"), mode="wb") as f:
            pickle.dump(self.detailedResults, file=f)

        with open(file=os.path.join(new_directory, "runHistory.csv"), mode="w", newline="\n") as f:
            for time, entry in self.runHistory:
                print(f"{time},{entry}", file=f)

        with open(file=os.path.join(new_directory, "readableResults.md"), mode="w", newline="\n") as f:
            print(self.currentResponse.results, file=f)
