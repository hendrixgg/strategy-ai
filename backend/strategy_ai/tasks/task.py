from abc import ABC, abstractmethod
from uuid import uuid4

# const response = {
#         status: "",
#         message: "",
#         date: "",
#         task_data: {
#             task_type_id: 0,
#             uuid: "",
#             progress_info: "",
#             results: "",
#             files_used: ["", ""],
#             metadata: {},
#         },
#     };


class BaseTask(ABC):
    def __init__(self, task_type: int, task_name: str):
        """must provide the task type and name.
        you also need to implement the generate_results method
        which is an iterator that will output the results of 
        running the task as it progresses"""
        self.task_type = task_type
        self.task_name = task_name
        self.unique_id = uuid4()
        # Should be what you would print to the console indicating what progress has been made so far, this variable can change over the course of running the task.
        self.progress_info = ""
        # Depends on the type of task, could be a string for text outputs, an of object for a file, etc. This variable may change over the course of running the task.
        self.results = None
        # folder indicating all the files that were available during the task execution
        self.files_used = {}
        # properties about the task being run, such as the parameters chosen to run the task, the date the task was run, etc.
        self.metadata = dict()

    @abstractmethod
    def generate_results(self):
        yield f"base task started, id: {self.unique_id}"
