import json
import os
from dataclasses import asdict

from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from strategy_ai.ai_core.data_sets.doc_store import DocStore, DocumentSource
from strategy_ai.ai_core.data_sets.vector_store import FAISSVectorStore
from strategy_ai.tasks.path_to_json import path_to_dict
from strategy_ai.tasks.t1_surfacing import Task1SurfacingTask
from strategy_ai.tasks.task import BaseTask, TaskStatus

# nltk.download("punkt")

# load environment variables for openai and other API keys
load_dotenv(verbose=True)

api = Flask(__name__)
CORS(api, origins="*")

# key: str = task uuid, value: BaseTask
# This stores the tasks that have been initalized in this session
tasks: dict[str, BaseTask] = dict()


# File system
# For now these directories are hardcoded, but in the future they could be accessed from a database
available_documents_directory = os.path.join(
    os.getcwd(), "strategy_ai", "available_data")

methodology_documents_directory = os.path.join(
    available_documents_directory, "hidden_files", "methodology_files")
client_documents_directory = os.path.join(
    available_documents_directory, "visible_files", "client_files")
ai_documents_directory = os.path.join(
    available_documents_directory, "visible_files", "ai_files")

ai_output_directory = os.path.join(
    available_documents_directory, "hidden_files", "ai_output")
vector_store_save_directory = os.path.join(
    available_documents_directory, "hidden_files", "vector_store_saves")

documents = DocStore(dict({
    "Methodology Documents": DocumentSource(name="Pm2 Methodology Documents", directory_path=methodology_documents_directory),
    "Client Documents": DocumentSource(name="Client Documents", directory_path=client_documents_directory),
    "Website Documents": DocumentSource(name="Website Documents", filePaths=[os.path.join(available_documents_directory, "visible_files", "weblinks.txt")]),
    "AI Documents": DocumentSource(name="AI Generated Documents", directory_path=ai_documents_directory)
}))

vectorStore = FAISSVectorStore(documents.splitDocuments)

llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)


@api.route("/files")
def files():
    return path_to_dict(os.getcwd(), os.path.join("strategy_ai", "available_data", "visible_files"))


@api.route("/init_task/<task_id>")
def init_task(task_id: int):
    """Instantiates the new task and returns the initial task info"""
    if task_id != "1":
        return {"status": "error", "message": "task not implemented"}
    newTask = Task1SurfacingTask(
        contextVectorStore=vectorStore,
        availableDataFolder=available_documents_directory,
        llm=llm
    )
    tasks[newTask.currentResponse.task_uuid] = newTask

    return asdict(newTask.currentResponse)


@api.route("/task_stream/<unique_id>")
def task_stream(unique_id: int):
    """Runs the task, returns a stream of the results as the task progresses."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return Response(tasks[unique_id].generate_results_json_bytes(saveDirectory=ai_output_directory))


@api.route("/task_results/<unique_id>")
def task_results(unique_id: str):
    """Returns the results of the task at the current time."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return asdict(tasks[unique_id].currentResponse)


@api.route("/save_results/<unique_id>", methods=["POST"])
def save_results(unique_id: str):
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    with open(f"{ai_documents_directory}\\Strategy_Surfacing_{tasks[unique_id].currentResponse.date.replace(':', '-')}_{tasks[unique_id].currentResponse.task_uuid}.md", "x") as f:
        print(tasks[unique_id].currentResponse.results, file=f)

    return {"status": "success", "message": "task results saved"}

# testing funcitons are below


@api.route("/test_stream/<length>")
def test_stream(length):
    """Returns a stream of json objects with the type "results_text" and the body as the number of the object."""
    def generator():
        for i in range(int(length)):
            jsonString = json.dumps(
                {"type": "results_text", "body": f"{i}"}) + "\n"
            yield bytes(jsonString, encoding="ascii")
    return Response(generator())


def recursive_dict_types(d: dict):
    """Returns a dictionary with the same structure as the input dictionary, but with the types of the values instead of the values themselves."""
    d_types = {}
    for key, value in d.items():
        if type(value) == dict:
            d_types[key] = recursive_dict_types(value)
        else:
            d_types[key] = type(value)
    return d_types


if __name__ == "__main__":
    newTask = Task1SurfacingTask(
        contextVectorStore=vectorStore,
        availableDataFolder=available_documents_directory,
        llm=llm
    )
    # print(newTask.currentResponse.files_available)
    for result in newTask.generate_results_json_bytes():
        print(result)
    #     newTask.currentResponse.update()
    #     with open(f"{ai_documents_directory}\\Strategy_Surfacing_{newTask.currentResponse.date.replace(':', '-')}_{newTask.currentResponse.task_uuid}.md", "x") as f:
    #         print("test", file=f)
