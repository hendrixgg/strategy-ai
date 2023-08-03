import datetime
import json
import os
import asyncio
from typing import Iterator
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage, FunctionMessage

from strategy_ai.ai_core import openai_chat
from strategy_ai.ai_core.data_sets.vector_store import FAISSVectorStore

from strategy_ai.tasks.task_models import TaskData, TaskState, TaskTypeEnum

load_dotenv(verbose=True)

# all asserts should be impossible if the code has no bugs


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
    if task.state != TaskState.FINISHED:
        raise Exception(
            "Cannot save the results since the task is not finished")

    new_directory = os.path.join(
        directory, f"{task.task_type.value.name}-{task.id}")
    os.mkdir(new_directory)

    with open(file=os.path.join(new_directory, "runHistory.csv"), mode="w", newline="\n") as f:
        for time, entry in task.run_history:
            print(f'{time},"{entry}"', file=f)

    with open(file=os.path.join(new_directory, "readableResults.md"), mode="w", newline="\n") as f:
        print(task.results_text, file=f)

    with open(file=os.path.join(new_directory, "detailedResults.json"), mode="wb") as f:
        f.write(bytes(task.json(
            exclude={"run_history", "results_text"}, indent=4), encoding="ascii"))


def _task_init_surfacing(task: TaskData, vector_store: FAISSVectorStore, llm=ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)) -> None:
    """This function is only called within task_init() and is used to initialize the tasks where task.task_type == TaskTypeEnum.SURFACING."""
    objectiveCategories = {
        "Financial": [
            "Increasing Revenue",
            "Cost Reduction",
            "Asset Optimization",
        ],
        "Customer": [
            "Improving the Brand",
            "Customer Service",
            "Product Service/Functionality",
        ],
        "Internal": [
            "Operational Excellence",
            "Product Innovation",
            "Regulatory Compliance",
            "Customer Intimacy",
        ],
        "Enabler": [
            "Strategic Assets",
            "Building a Climate for Action",
            "Attracting, Retaining, and Developing Talent",
        ]
    }
    system_message_prompt_template = """Use the following pieces of context to answer the user's question.
Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "I don't know", don't try to make up an answer.

----------------
{context}
"""
    list_objectives_prompt_template = """Provide a list of this company's objectives addressing {topic}, in an organized format.
If there is a function provided, use the function.
Lastly, aim to identify 2-3 objetives. If you cannot find objectives on the topic of {topic}, list some relevant suggestions based on the context.
"""
    objectives_format = {
        "name": "output_formatted_objectives",
        "description": "given a list of objectives for a business in the format of [Verb] [Outcome] [Definition] [Source], print it to the screen.",
        "parameters": {
            "type": "object",
            "properties": {
                "objectives_list": {
                    "type": "array",
                    "minItems": 1,
                    "description": "a list of all the formatted objectives, including the source file for each objective or a direct quote",
                    "items": {
                        "title": "Objective",
                        "type": "object",
                        "properties": {
                            "Verb": {
                                "type": "string",
                                "decription": "A single word describing an action. A verb in present tense, not present continous tense, just present tense",
                            },
                            "Outcome": {
                                "type": "string",
                                "decription": "One or 2 words which are the outcome of this objective",
                            },
                            "Definition": {
                                "type": "string",
                                "description": "Definition should anser these two questions in two sentences: What is the objective working to achieve? Why is the objective important to the business?",
                            },
                            "Source": {
                                "type": "string",
                                "description": "the complete file name where this objective was found, or directly quoted text",
                            },
                        },
                    },
                },
            },
        },
        "required": ["objectives_list"],
    }

    def topic_messages(topic: str) -> list[dict | list]:
        sys_msg = SystemMessage(content=system_message_prompt_template.format(
            context=vector_store.formatted_context(topic)))
        hmn_msg = HumanMessage(
            content=list_objectives_prompt_template.format(topic=topic))

        return [
            {
                "type": openai_chat.MessageRole.SYSTEM,
                "title": "Context",
                "body": sys_msg.content,
            },
            {
                "type": openai_chat.MessageRole.HUMAN,
                "title": "Human Prompt",
                "body": hmn_msg.content,
            },
            [
                {
                    "type": openai_chat.MessageRole.ASSISTANT,
                    "title": "Text Response",
                    "body": None,
                    "task": None,
                    "coro": llm.apredict_messages(messages=[sys_msg, hmn_msg]),
                },
                {
                    "type": openai_chat.MessageRole.ASSISTANT,
                    "title": "Formatted Response",
                    "body": None,
                    "task": None,
                    "coro": llm.apredict_messages(
                        messages=[sys_msg, hmn_msg],
                        functions=[objectives_format],
                        function_call={"name": "output_formatted_objectives"}),
                },
            ],
        ]

    def category_topics(topics: list[str]) -> dict[str, dict]:
        return {
            topic: {
                "title": f"topic: {topic}",
                "body": topic_messages(topic),
            }
            for topic in topics
        }

    task.detailed_results = {
        "title": "Company Objectives",
        "body": {
            category: {
                "title": f"Category: {category}",
                "body": category_topics(topics),
            }
            for category, topics in objectiveCategories.items()
        }
    }


def _task_init_assessment(task: TaskData, vector_store: FAISSVectorStore, llm=ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)) -> None:
    """This function is only called within task_init() and is used to initialize the tasks where task.task_type == TaskTypeEnum.ASSESSMENT."""
    # For now, the goals are just hard coded. Normally the goals would start as an empty list and the llm and vector store would be used to generate the goals.
    goals = [
        "increase sales revenue by 20% compared to last year (from 10M to 12M)"]
    # these are the prompts that could be used to generate the actions that would help achieve a goal
    business_expert_system_message_template = "You are a business expert and you are helping a company achieve the following goal: {goal}"
    list_actions_prompt_template = "List actions that could be taken to achieve the following goal: {goal}"
    use_formatting_function_prompt = "TIP: Use the {function_name} function to format your response to the user."
    formatted_actions_list = {
        "name": "formatted_actions_list",
        "description": "Use this function to output the formatted list of actions to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "actions_list": {
                    "title": "Actions List",
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        },
        "required": ["actions_list"],
    }
    providing_context_system_message_template = """Use the following pieces of context to answer the user's question.
Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "I don't know", don't try to make up an answer.

----------------
{context}
"""
    look_into_action_prompt_template = """List all the things that the company is doing or has planned to do to carry out the following action: {action}.
Beside each point answer the following questions:
- will this make a difference (refer to what the company has done in previous years and what their competitors are doing)?
- what additional resources does the company require to carry this out?
- what regulations need to be followed?
- what similar things have competing businesses done?
"""

    # summarize_actions_prompt_template = """Based the actions listed below, provide a short summary indicating whether or not it is feasible for "{goal}" to be achieved. \nActions and pertinent info:\n{actions_and_info}"""

    def action_info(action: str) -> list[dict | list]:
        human_message = HumanMessage(
            content=look_into_action_prompt_template.format(action=action))
        system_message = SystemMessage(content=providing_context_system_message_template.format(
            context=vector_store.formatted_context(human_message.content)))
        return [
            {
                "type": openai_chat.MessageRole.SYSTEM,
                "title": "Context",
                "body": system_message.content,
            },
            {
                "type": openai_chat.MessageRole.HUMAN,
                "title": "Human Message",
                "body": human_message.content,
            },
            [
                {
                    "type": openai_chat.MessageRole.ASSISTANT,
                    "title": "Text Response",
                    "body": None,
                    "task": None,
                    "coro": llm.apredict_messages([system_message, human_message]),
                },
                {
                    "type": openai_chat.MessageRole.ASSISTANT,
                    "title": "Formatted Response",
                    "body": None,
                    "task": None,
                    "coro": None,
                },
            ]
        ]

    def goal_summary(actions: list[str]) -> str:
        return {
            action: {
                "title": f"Action: {action}",
                "body": action_info(action),
            } for action in actions
        }

    async def get_actions(goal: str) -> list[str]:
        """As of now, this assumes that the goal is always: increase sales revenue by X% compared to last year.
        """
        await asyncio.sleep(0.1)
        list_of_actions = [
            "increase headcount",
            "increase price",
            "enter new markets",
            "introduce new products",
            "combination",
            "increase customer retention / decrease churn",
        ]
        # list_of_actions = await llm.apredict_messages([
        #     SystemMessage(
        #         content=business_expert_system_message_template.format(goal=goal)),
        #     HumanMessage(
        #         content=list_actions_prompt_template.format(goal=goal)),
        #     SystemMessage(use_formatting_function_prompt.format(
        #         function_name=formatted_actions_list["name"])),
        # ], functions=[formatted_actions_list], function_call="auto").additional_kwargs.get(
        #     "function_call").get("arguments").get("actions_list")
        return list_of_actions

    task.detailed_results = {
        "title": "Feasibility Assessment on the company's goals",
        "body": {
            goal: {
                "title": f"Goal Assessment for: {goal}",
                "body": goal_summary,
                "task": None,
                "coro": get_actions(goal),
            } for goal in goals
        },
        "task": None,
        "coro": None,
    }


def task_init(task: TaskData, vector_store: FAISSVectorStore, llm: ChatOpenAI) -> None:
    """This function will initialize the task.

    It will call the task specific initialization function depeding on `task.task_type`. 

    The task specific initalizer must set the task state to ready.

    Args:
        `task`: A task.TaskData instance to be initialized. **Required for all tasks.**

        `vector_store`: A vector_store.FAISSVectorStore instance to be used for the task. Required for all tasks.

        `llm`: A llm instance to be used for the task. This should be ChatOpenAI(model="gpt-3.5-turbo-0613") or some model that supports function calling. Required for all tasks.

    Returns:
        None

    Raises:
        Exception: If the task is not in the preparing state before calling this function.
        Exception: If the task state was changed while running the task specific initalizer.
    """
    if task.state != TaskState.PREPARING:
        raise Exception(
            f"Cannot initialize task {task.task_type.value.name}, uuid: {task.id}, state: {task.state}. It needs to be in the preparing state.")

    match task.task_type:
        case TaskTypeEnum.SURFACING:
            _task_init_surfacing(task, vector_store, llm)
        case TaskTypeEnum.ASSESSMENT:
            _task_init_assessment(task, vector_store, llm)
        case _:
            raise Exception(f"invalid task type: {task.task_type}")

    # ensure that the task state was not changed in the task specific initializer
    assert task.state == TaskState.PREPARING

    task.state = TaskState.READY


def _task_generate_results_surfacing(task: TaskData) -> Iterator[dict]:
    """ Generate the results for the task.
    """
    prefix = "## "
    yield {"type": "message", "body": f"Running task {task.task_type.name}, uuid: {task.id}."}
    yield {"type": "results_text", "body": prefix + task.detailed_results["title"]}

    # creating all the async tasks
    async_event_loop = asyncio.new_event_loop()
    for categoryInfo in task.detailed_results["body"].values():
        for topicInfo in categoryInfo["body"].values():
            # iterate over list of messages for the different responses from the AI
            for message in topicInfo["body"][2]:
                message["task"] = async_event_loop.create_task(
                    message["coro"])

    # generating the results
    for category, categoryInfo in task.detailed_results["body"].items():
        prefix = "### "
        yield {"type": "progress_info", "body": f"{category} objectives complete:"}
        yield {"type": "results_text", "body": prefix + categoryInfo["title"]}
        for topic, topicInfo in categoryInfo["body"].items():
            prefix = "#### "
            yield {"type": "results_text", "body": prefix + topicInfo["title"]}
            prefix = "##### "
            # iterate over the messages for the different responses from the AI
            for aiMessage in topicInfo["body"][2]:
                yield {"type": "results_text", "body": prefix + aiMessage["title"]}
                # wait until the coroutine has completed
                aiMessage["body"] = async_event_loop.run_until_complete(
                    aiMessage["task"])
                del aiMessage["task"], aiMessage["coro"]
                if aiMessage["title"] == "Formatted Response":
                    aiMessage["body"] = json.loads(aiMessage["body"].additional_kwargs.get(
                        "function_call").get("arguments"))["objectives_list"]
                    yield {"type": "results_text", "body": f"```json\n{json.dumps(aiMessage['body'], indent=4)}\n```"}
                elif aiMessage["title"] == "Text Response":
                    aiMessage["body"] = aiMessage["body"].content
                    yield {"type": "results_text", "body": f"```text\n{aiMessage['body']}\n```"}

            yield {"type": "progress_info", "body": f"- {topic}"}


def _task_generate_results_assessment(task: TaskData) -> Iterator[dict]:
    """This function is used to generate the results of the task."""
    prefix = "## "
    yield {"type": "message", "body": f"Running task {task.task_type.name}, uuid: {task.id}."}
    yield {"type": "results_text", "body": prefix + task.detailed_results["title"]}

    # creating all the async tasks
    async_event_loop = asyncio.get_event_loop()
    for goal, goal_dict in task.detailed_results["body"].items():
        # this callback adds the llm calls about the actions to the even loop
        async def goal_subtasks():
            # before this line goal_dict["body"] is the function goal_summary
            # calling it creates the summary which is a dict of action-info pairs
            goal_dict["body"] = goal_dict["body"](await goal_dict["coro"])
            for action_info in goal_dict["body"].values():
                # iterate over list of messages for the responses from the AI
                for message in action_info["body"][2]:
                    if message["coro"] is not None:
                        message["task"] = async_event_loop.create_task(
                            message["coro"])

        goal_dict["task"] = async_event_loop.create_task(
            goal_subtasks())

    for goal, goal_dict in task.detailed_results["body"].items():
        prefix = "### "
        yield {"type": "progress_info", "body": f"{goal}; actions assessed:"}
        yield {"type": "results_text", "body": prefix + goal_dict["title"]}
        # wait for the goal actions to be created
        async_event_loop.run_until_complete(
            goal_dict["task"])
        # to ensure the results are pickleable
        del goal_dict["task"], goal_dict["coro"]
        for action_info in goal_dict["body"].values():
            prefix = "#### "
            yield {"type": "results_text", "body": prefix + action_info["title"]}
            # wait for the action to be assessed
            action_info["body"][2][0]["body"] = async_event_loop.run_until_complete(
                action_info["body"][2][0]["task"]).content
            # to ensure the results are pickleable
            del action_info["body"][2][0]["task"], action_info["body"][2][0]["coro"]
            yield {"type": "results_text", "body": action_info["body"][2][0]["body"]}


def task_generate_results(task: TaskData) -> Iterator[dict]:
    """This function will return a generator that will yield the dictionaries that can be sent to the frontend.

    Tasks should only be run once, and this function should only be called once per task.

    Args:
        `task`: a TaskData instance to be referenced. This is the task that will be run.

    Returns:
        A generator that will yield the dictionaries that can be sent to the frontend.

    Raises:
        AssertionError: If the task is not in the ready state when this function is called.
        Exception: If the task was set to Finished when the task specific results were being generated.
    """
    assert task.state == TaskState.READY, f"Task is not ready to run. Current state: {task.state}"

    task.message = f"Starting task {task.task_type.value.name}, uuid: {task.id}."
    task.state = TaskState.RUNNING
    task.date_start = datetime.datetime.now()
    yield {"type": "message", "body": task.message}

    # this is where the detailed_results are generated
    # perhaps some messages and progress_info results are generated here also
    # you must ensure that after these results are generated, that the task.detailed_results are pickleable (i.e. no lambda functions)
    match task.task_type:
        case TaskTypeEnum.SURFACING:
            yield from _task_generate_results_surfacing(task)
        case TaskTypeEnum.ASSESSMENT:
            yield from _task_generate_results_assessment(task)
        case _:
            assert False, f"Task type {task.task_type.value.name} not implemented."

    assert task.state == TaskState.RUNNING, f"Task {task.task_type.value.name} state should not have changed while running, uuid: {task.id}, state: {task.state}."

    yield {"type": "message", "body": f"Finished task {task.task_type.value.name}, uuid: {task.id}. It took {task.date_recent - task.date_start}."}
    task.state = TaskState.FINISHED


def task_generate_results_with_processing(task: TaskData, save_directory: str | None = None) -> Iterator[dict]:
    """This function will update the task as the results are generated and yielded.

    Args:
        `task`: TaskData instance to be referenced. This is the task that is being run.

        `save_directory`: A string representing the directory to save the results to. If None, the results will not be saved.

    Returns:
        A generator of dicts which are all the results of the task.

        each dict is of the format: {"type": str, "body": str} 
        where type is one of: "results_text", "progress_info", "message"

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
                assert False, f"Unknown result type: {result['type']}."
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
    yield from (bytes(json.dumps(d) + "\n", encoding="ascii") for d in dict_iter)
