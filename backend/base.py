from dataclasses import asdict
import json

from flask import Flask, Response
from flask_cors import CORS

from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv

from strategy_ai.tasks.task import TaskStatus
from strategy_ai.ai_core.data_sets.doc_store import DocStore, DocumentSource
from strategy_ai.ai_core.data_sets.vector_store import FAISSVectorStore
from strategy_ai.tasks.path_to_json import path_to_dict
from strategy_ai.tasks.task import BaseTask
from strategy_ai.tasks.t1_surfacing import T1SurfacingTask

# nltk.download("punkt")

# load environment variables for openai and other API keys
load_dotenv(verbose=True)

api = Flask(__name__)
CORS(api, origins="*")

# key: str = task uuid, value: BaseTask
tasks: dict[str, BaseTask] = dict()

# set up AI objects, documents, vector store, llm
available_docuements_directory = "C:\\Users\\Hendrix\\Documents\\GitHub\\strategy-ai\\backend\\strategy_ai\\available_data"
methodology_documents_directory = f"{available_docuements_directory}\\hidden_files\\methodology_files"
client_documents_directory = f"{available_docuements_directory}\\visible_files\\client_files"
ai_documents_directory = f"{available_docuements_directory}\\visible_files\\ai_files"

ai_output_directory = f"{available_docuements_directory}\\hidden_files\\ai_output"
vector_store_save_directory = f"{available_docuements_directory}\\hidden_files\\vector_store_saves"

documents = DocStore(dict({
    "Methodology Documents": DocumentSource(name="Pm2 Methodology Documents", directory_path=methodology_documents_directory),
    "Client Documents": DocumentSource(name="Documents from aFe", directory_path=client_documents_directory),
    "AI Documents": DocumentSource(name="AI Generated Documents", directory_path=ai_documents_directory)
}))

vectorStore = FAISSVectorStore(
    documents.splitDocuments)

llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)


@api.route("/files")
def files():
    return path_to_dict(f".\\strategy_ai\\available_data\\visible_files")


@api.route("/init_task/<task_id>")
def init_task(task_id: int):
    """Instantiates the new task and returns the initial task info"""
    if task_id != "1":
        return {"status": "error", "message": "task not implemented"}
    newTask = T1SurfacingTask(
        contextVectorStore=vectorStore,
        availableDataFolder=available_docuements_directory,
        llm=llm
    )
    tasks[newTask.currentResponse.task_uuid] = newTask

    return asdict(newTask.currentResponse)


@api.route("/task_stream/<unique_id>")
def task_stream(unique_id: int):
    """Runs the task, returns a stream of the results as the task progresses."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return Response(tasks[unique_id].generate_results_json_bytes())


@api.route("/task_results/<unique_id>")
def task_results(unique_id: str):
    """Returns the results of the task at the current time."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return asdict(tasks[unique_id].currentResponse)


@api.route("/save_results/<unique_id>")
def save_results(unique_id: str):
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    with open(f"{ai_documents_directory}\\Strategy_Surfacing_{tasks[unique_id].currentResponse.date.replace(':', '-')}_{tasks[unique_id].currentResponse.task_uuid}.md", "x") as f:
        print(tasks[unique_id].currentResponse.results, file=f)

    return {"status": "success"}


def recursive_dict_types(d: dict):
    d_types = {}
    for key, value in d.items():
        if type(value) == dict:
            d_types[key] = recursive_dict_types(value)
        else:
            d_types[key] = type(value)
    return d_types


# if __name__ == "__main__":
#     newTask = T1SurfacingTask(
#         contextVectorStore=vectorStore,
#         availableDataFolder=available_docuements_directory,
#         llm=llm
#     )
#     newTask.currentResponse.update()
#     with open(f"{ai_documents_directory}\\Strategy_Surfacing_{newTask.currentResponse.date.replace(':', '-')}_{newTask.currentResponse.task_uuid}.md", "x") as f:
#         print("test", file=f)
