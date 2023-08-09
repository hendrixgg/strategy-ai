import json
import os

from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from strategy_ai import (
    FAISSVectorStore,
    DocStore,
    DocumentSource,
    TaskData,
    TaskTypeEnum,
    task_init,
    task_generate_results_with_processing,
    dict_iter_ndjson_bytes,
    path_to_file_struct,
)

# nltk.download("punkt")

# load environment variables for openai and other API keys
load_dotenv(verbose=True)

api = Flask(__name__)
CORS(api, origins="*")

# File system
# For now these directories are hardcoded, but in the future they could be accessed from a database
backend_directory = os.path.dirname(__file__)
available_documents_directory = os.path.join(
    backend_directory, "strategy_ai", "available_data")
hidden_files_directory = os.path.join(
    available_documents_directory, "hidden_files")
visible_files_directory = os.path.join(
    available_documents_directory, "visible_files")

methodology_documents_directory = os.path.join(
    hidden_files_directory, "methodology_files")
client_documents_directory = os.path.join(
    visible_files_directory, "client_files")
ai_documents_directory = os.path.join(visible_files_directory, "ai_files")

ai_output_directory = os.path.join(hidden_files_directory, "ai_output")
vector_store_save_directory = os.path.join(
    hidden_files_directory, "vector_store_saves")

# loading documents from files
documents = DocStore(dict({
    "Methodology Documents": DocumentSource(name="Pm2 Methodology Documents", directory_path=methodology_documents_directory),
    "Client Documents": DocumentSource(name="Client Documents", directory_path=client_documents_directory),
    "Website Documents": DocumentSource(name="Website Documents", filePaths=[os.path.join(available_documents_directory, "visible_files", "weblinks.txt")]),
    "AI Documents": DocumentSource(name="AI Generated Documents", directory_path=ai_documents_directory)
}))

# vector store to allow for document similarity search
vectorStore = FAISSVectorStore(documents.splitDocuments)

# language model for chat
llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)

# key: str = task uuid, value: TaskData
# This stores the tasks that have been initalized in this session
tasks: dict[str, TaskData] = dict()

task_type_id_to_task_type = [
    0,
    TaskTypeEnum.SURFACING,
    TaskTypeEnum.ASSESSMENT
]


@api.route("/files")
def files():
    return path_to_file_struct(backend_directory, os.path.relpath(visible_files_directory, backend_directory)).dict(by_alias=True)


@api.route("/init_task/<task_type_id>")
def init_task(task_type_id: str):
    """Instantiates the new task and returns the initial task info"""
    task_type_id = int(task_type_id)
    if task_type_id < 1 or 2 < task_type_id:
        return {"status": "error", "message": "task not implemented"}

    newTask = TaskData(
        task_type=task_type_id_to_task_type[task_type_id],
        files_available=path_to_file_struct("", available_documents_directory))
    task_init(newTask, vector_store=vectorStore, llm=llm)

    tasks[str(newTask.id)] = newTask

    return Response(newTask.json(include={"id", "task_type", "date_recent"}), mimetype="application/json")


@api.route("/task_stream/<unique_id>")
def task_stream(unique_id: str):
    """Runs the task, returns a stream of the results as the task progresses."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return Response(dict_iter_ndjson_bytes(task_generate_results_with_processing(tasks[unique_id], save_directory=ai_output_directory)))


@api.route("/task_results/<unique_id>")
def task_results(unique_id: str):
    """Returns the results of the task at the current time."""
    if unique_id not in tasks:
        return {"status": "error", "message": "task not initialized"}
    return tasks[unique_id].json(exclude={"detailed_results"})


@api.route("/save_results/<unique_id>", methods=["POST"])
def save_results_to_ui(unique_id: str):
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    with open(f"{ai_documents_directory}\\{tasks[unique_id].task_type.value.name}_{str(tasks[unique_id].date_recent).replace(':', '-')}_{unique_id}.md", "x") as f:
        print(tasks[unique_id].results_text, file=f)

    return {"status": "success", "message": "task results saved"}

# testing funcitons are below


@api.route("/test_stream/<length>")
def test_stream(length):
    """Returns a stream of json objects with the type "results_text" and the body as the number of the object."""
    def generator():
        for i in range(int(length)):
            yield bytes(json.dumps({"type": "results_text", "body": f"{i}"}) + "\n", encoding="ascii")
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
    import uuid
    newTask = TaskData(
        task_type=TaskTypeEnum.SURFACING,
        files_available=path_to_file_struct(available_documents_directory),
        id=str(uuid.uuid4())
    )

    task_init(newTask, vector_store=vectorStore, llm=llm)
    for result in task_generate_results_with_processing(newTask, save_directory=ai_output_directory):
        print("result")
#     bad_json_str = '{"path": "C:\\Users\\Hendrix\\Documents\\GitHub\\strategy-ai\\frontend"}'
#     try:
#         parsed_json = json.loads(bad_json_str)
#     except json.decoder.JSONDecodeError as e:
#         error_message = str(e)
#         print(repr(e))
#         if error_message.startswith("Invalid \\escape:"):
#             parsed_json = json.loads(
#                 bad_json_str.replace("\\", "\\\\"))
#             print(
#                 f"Corrected the following error: {type(e)} {error_message}")
#         else:
#             raise e
#     print(parsed_json)
    # print(newTask.dict(include={"id", "task_type", "date_recent"}))
    # list_of_actions = llm.predict_messages([
    #     SystemMessage(
    #         content=business_expert_system_message_template.format(goal=goals[0])),
    #     HumanMessage(
    #         content=list_actions_prompt_template.format(goal=goals[0])),
    #     SystemMessage(
    #         content=use_formatting_function_prompt.format(function_name=formattedActionsList.get("name")))
    # ],
    #     functions=[formattedActionsList], function_call={"name": formattedActionsList.get("name")})

    # print([list_of_actions])
    # print([AIMessage(content="test")])
