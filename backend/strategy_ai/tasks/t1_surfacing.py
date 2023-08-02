import asyncio
from typing import Iterator

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, SystemMessage, BaseMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

from strategy_ai.ai_core import openai_chat
from strategy_ai.ai_core.data_sets.vector_store import FAISSVectorStore

from strategy_ai.tasks.task import TaskState, TaskData

load_dotenv(verbose=True)


def task1_init(task: TaskData, vector_store: FAISSVectorStore, llm=ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)):
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
                "body": sys_msg,
            },
            {
                "type": openai_chat.MessageRole.HUMAN,
                "title": "Human Prompt",
                "body": hmn_msg,
            },
            [
                {
                    "type": openai_chat.MessageRole.ASSISTANT,
                    "title": "Text Response",
                    "body": None,
                    "async": llm.apredict_messages(messages=[sys_msg, hmn_msg]),
                },
                {
                    "type": openai_chat.MessageRole.ASSISTANT,
                    "title": "Formatted Response",
                    "body": None,
                    "async": llm.apredict_messages(
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


def task1_generate_results(task: TaskData):
    """ Generate the results for the task.
    """
    prefix = "## "
    yield {"type": "message", "body": f"Running task {task.task_type.name}, uuid: {task.id}."}
    yield {"type": "results_text", "body": prefix + task.detailed_results["title"]}

    # creating all the async tasks
    asyncEventLoop = asyncio.new_event_loop()
    for categoryInfo in task.detailed_results["body"].values():
        for topicInfo in categoryInfo["body"].values():
            # iterate over list of messages for the different responses from the AI
            for message in topicInfo["body"][2]:
                message["async"] = asyncEventLoop.create_task(
                    message["async"])

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
                aiMessage["body"] = asyncEventLoop.run_until_complete(
                    aiMessage["async"])
                del aiMessage["async"]
                if aiMessage["type"] == "text_response":
                    yield {"type": "results_text", "body": "```text\n" + aiMessage["body"].content + "\n```"}
                elif aiMessage["type"] == "function_response":
                    yield {"type": "results_text", "body": "```json\n" + aiMessage["body"].additional_kwargs.get(
                        "function_call").get("arguments") + "\n```"}

            yield {"type": "progress_info", "body": f"- {topic}"}
