import openai
from langchain.schema import HumanMessage, SystemMessage, AIMessage, FunctionMessage
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
from strategy_ai.tasks.t1_surfacing import Task1Surfacing
from strategy_ai.tasks.t2_assessment import Task2Assessment
from strategy_ai.tasks.task import TaskData, TaskTypeEnum, task_init, task_generate_results_with_processing, dict_iter_ndjson_bytes

# nltk.download("punkt")

# load environment variables for openai and other API keys
load_dotenv(verbose=True)

api = Flask(__name__)
CORS(api, origins="*")

# key: str = task uuid, value: TaskData
# This stores the tasks that have been initalized in this session
tasks: dict[str, TaskData] = dict()


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


task_type_id_to_task_type = [
    0,
    TaskTypeEnum.SURFACING,
    TaskTypeEnum.ASSESSMENT
]


@api.route("/init_task/<task_type_id>")
def init_task(task_type_id: str):
    """Instantiates the new task and returns the initial task info"""
    task_type_id = int(task_type_id)
    if task_type_id < 1 or 2 < task_type_id:
        return {"status": "error", "message": "task not implemented"}

    newTask = TaskData(task_type=task_type_id_to_task_type[task_type_id], files_available=path_to_dict(
        available_documents_directory))
    task_init(newTask, vector_store=vectorStore, llm=llm)

    tasks[newTask.id] = newTask

    return newTask.json(exclude={"detailed_results"})


@api.route("/task_stream/<unique_id>")
def task_stream(unique_id: int):
    """Runs the task, returns a stream of the results as the task progresses."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return Response(dict_iter_ndjson_bytes(task_generate_results_with_processing(tasks[unique_id])))


@api.route("/task_results/<unique_id>")
def task_results(unique_id: str):
    """Returns the results of the task at the current time."""
    if unique_id not in tasks.keys():
        return {"status": "error", "message": "task not initialized"}
    return asdict(tasks[unique_id].currentResponse)


@api.route("/save_results/<unique_id>", methods=["POST"])
def save_results_to_ui(unique_id: str):
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
    newTask = Task2Assessment(
        contextVectorStore=vectorStore,
        availableDataFolder=available_documents_directory,
        llm=llm
    )
    for result in newTask.generate_results(saveDirectory=ai_output_directory):
        print(result)
    # print(newTask.currentResponse.files_available)
    # for result in newTask.generate_results_json_bytes():
    #     print(result)
    #     newTask.currentResponse.update()
    #     with open(f"{ai_documents_directory}\\Strategy_Surfacing_{newTask.currentResponse.date.replace(':', '-')}_{newTask.currentResponse.task_uuid}.md", "x") as f:
    #         print("test", file=f)
    # goals = [
    #     "increase sales revenue by 20% compared to last year (from 10M to 12M)"]
    # business_expert_system_message_template = "You are a business expert and you are helping a company achieve the following goal: {goal}"
    # list_actions_prompt_template = "List actions that could be taken to achieve the following goal: {goal}"
    # use_formatting_function_prompt = "TIP: Use the {function_name} function to format your response to the user."
    # formattedActionsList = {
    #     "name": "formatted_actions_list",
    #     "description": "Use this function to output the formatted list of actions to the user.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "actions_list": {
    #                 "title": "Actions List",
    #                 "type": "array",
    #                 "items": {"type": "string"},
    #             },
    #         },
    #     },
    #     "required": ["actions_list"],
    # }
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
