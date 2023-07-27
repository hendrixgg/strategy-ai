import asyncio
import time

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, SystemMessage, BaseMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

from strategy_ai.ai_core.data_sets.vector_store import FAISSVectorStore

from strategy_ai.tasks.task import BaseTask
from strategy_ai.tasks.task import TaskStatus

load_dotenv(verbose=True)


class Task1SurfacingTask(BaseTask):
    def __init__(self, contextVectorStore: FAISSVectorStore, availableDataFolder: str, llm=ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)):
        """If the saveDirectory is provided, the results will be saved at the end of running the task"""
        super().__init__(1, "t1_surfacing", availableDataFolder)
        self.vectorStore = contextVectorStore
        self.llm = llm
        self.objectiveCategories = {
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
        self.system_message_prompt_template = """Use the following pieces of context to answer the users question.
Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "I don't know", don't try to make up an answer.

----------------
{context}
"""

        self.list_objectives_prompt_template = """Provide a list of this company's objectives addressing {topic}, in an organized format.
If there is a function provided, use the function.
Lastly, aim to identify 2-3 objetives. If you cannot find objectives on the topic of {topic}, list some relevant suggestions based on the context.
"""
        self.functionDescriptions = [
            {
                "name": "display_formatted_objectives",
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
                                        "description": "the complete file name in which this objective was found, or directly quoted text",
                                    },
                                },
                            },
                        },
                    },
                },
                "required": ["objectives_list"],
            },
        ]

        def topic_messages(topic: str):
            sys_msg = SystemMessagePromptTemplate.from_template(
                self.system_message_prompt_template).format(context=self.vectorStore.formatted_context(topic))
            hmn_msg = HumanMessagePromptTemplate.from_template(
                self.list_objectives_prompt_template).format(topic=topic)

            return [
                {
                    "type": "SystemMessage",
                    "title": "Context",
                    "body": sys_msg,
                },
                {
                    "type": "HumanMessage",
                    "title": "Human Prompt",
                    "body": hmn_msg,
                },
                [
                    {
                        "type": "text_response",
                        "title": "Text Response",
                        "body": None,
                        "task": None,
                        "coro": self.llm.apredict_messages(messages=[sys_msg, hmn_msg]),
                    },
                    {
                        "type": "function_response",
                        "title": "Function Response",
                        "body": None,
                        "task": None,
                        "coro": self.llm.apredict_messages(
                            messages=[sys_msg, hmn_msg],
                            functions=self.functionDescriptions,
                            function_call="auto"),
                    },
                ],
            ]

        def category_topics(topics: list[str]):
            return {
                topic: {
                    "title": f"topic: {topic}",
                    "body": topic_messages(topic),
                }
                for topic in topics
            }
        self.detailedResults = {
            "title": "Company Objectives",
            "body": {
                category: {
                    "title": f"Category: {category}",
                    "body": category_topics(topics),
                }
                for category, topics in self.objectiveCategories.items()
            }
        }
        self.currentResponse.status = TaskStatus.READY

    async def generate_results(self, saveDirectory: str | None = None):
        for response in super().generate_results():
            yield response

        prefix = "## "
        yield {"type": "message", "body": f"Running task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}."}
        yield {"type": "results_text", "body": prefix + self.detailedResults["title"]}
        for categoryInfo in self.detailedResults["body"].values():
            for topicInfo in categoryInfo["body"].values():
                for message in topicInfo["body"][2]:
                    message["task"] = asyncio.create_task(message["coro"])
        for category, categoryInfo in self.detailedResults["body"].items():
            prefix = "### "
            yield {"type": "progress_info", "body": f"{category} objectives complete:"}
            yield {"type": "results_text", "body": prefix + categoryInfo["title"]}
            for topic, topicInfo in categoryInfo["body"].items():
                prefix = "#### "
                yield {"type": "results_text", "body": prefix + topicInfo["title"]}
                prefix = "##### "
                for aiMessage in topicInfo["body"][2]:
                    yield {"type": "results_text", "body": prefix + aiMessage["title"]}
                    # wait until the coroutine has completed the text response for this topic
                    aiMessage["body"] = await aiMessage["task"]
                    del aiMessage["task"], aiMessage["coro"]
                    if aiMessage["type"] == "text_response":
                        yield {"type": "results_text", "body": "```text\n" + aiMessage["body"].content + "\n```"}
                    elif aiMessage["type"] == "function_response":
                        yield {"type": "results_text", "body": "```json\n" + aiMessage["body"].additional_kwargs.get(
                            "function_call").get("arguments") + "\n```"}

                yield {"type": "progress_info", "body": f"- {topic}"}

        self.currentResponse.status = TaskStatus.FINISHED

        self.save(saveDirectory) if saveDirectory else 0

        yield {"type": "message", "body": f"Finished task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}."}
