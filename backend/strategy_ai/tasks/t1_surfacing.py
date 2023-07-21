from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, SystemMessage
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


class T1SurfacingTask(BaseTask):
    def __init__(self, contextVectorStore: FAISSVectorStore, availableDataFolder: str, llm=ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)):
        super().__init__(1, "t1_surfacing", availableDataFolder)
        self.vectorStore = contextVectorStore
        self.llm = llm
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
        system_message_context_template = """Use the following pieces of context to answer the users question.
        Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
        If you don't know the answer, just say that "I don't know", don't try to make up an answer.

        ----------------
        {context}
        """

        list_objectives_prompt_template = """Provide a list of this company's objectives addressing {topic}, in an organized format.
        If there is a function provided, use the function.
        Lastly, aim to identify 2-3 objetives. If you cannot find objectives on the topic of {topic}, list some relevant suggestions based on the context.
        """
        self.promptTemplate = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                system_message_context_template),
            HumanMessagePromptTemplate.from_template(
                list_objectives_prompt_template),
        ])
        self.objectiveCategories = {
            "financial": [
                "increasing revenue",
                "cost reduction",
                "asset optimization",
            ],
            "customer": [
                "improving the brand",
                "Customer Service",
                "Product Service/Functionality",
            ],
            "internal": [
                "Operational Excellence",
                "Product Innovation",
                "Regulatory Compliance",
                "Customer Intimacy",
            ],
            "enabler": [
                "Strategic Assets",
                "building a climate for action",
                "attracting, retaining, and developing talent",
            ]
        }
        self.currentResponse.status = TaskStatus.READY
        self.detailedResults = {}

    def generate_results(self):
        for response in super().generate_results():
            yield response

        self.currentResponse.results += "## Company Objectives\n"
        self.currentResponse.message = f"Running task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}."
        yield self.currentResponse
        for category, topics in self.objectiveCategories.items():
            self.currentResponse.results += f"### Category: {category}\n"
            self.currentResponse.progress_info += f"{category} objectives complete:\n"
            yield self.currentResponse

            self.detailedResults[category] = {}
            for topic in topics:
                messages = self.promptTemplate.format_messages(
                    context=self.vectorStore.formatted_context(topic),
                    topic=topic
                )

                self.currentResponse.results += f"""#### topic: {topic}
                ##### context given
                ```text
                {messages[0].content}
                ```

                ##### human prompt
                ```text
                {messages[1].content}
                ```
                """
                yield self.currentResponse

                messages.append([self.llm.predict_messages(messages)])
                self.currentResponse.results += f"""
                ##### text_response
                ```text
                {messages[2][0].content}
                ```
                """
                yield self.currentResponse

                messages[2].append(self.llm.predict_messages(
                    messages=messages[0:2],
                    functions=self.functionDescriptions,
                    function_call="auto"
                ))
                self.currentResponse.results += f"""
                ##### function_response
                ```text
                {messages[2][1].additional_kwargs.get("function_call").get("arguments")}
                ```
                """
                yield self.currentResponse

                self.detailedResults[category][topic] = {
                    "context_given": messages[0],
                    "human_question": messages[1],
                    "text_response": messages[2][0],
                    "function_response": messages[2][1],
                }
                self.currentResponse.progress_info += f"- {topic}\n"
                yield self.currentResponse

        self.currentResponse.status = TaskStatus.FINISHED
        self.currentResponse.message = f"Finished task {self.currentResponse.task_name}, uuid: {self.currentResponse.task_uuid}."
        yield self.currentResponse

    def save_results(self, filePath: str):
        if self.currentResponse.status != TaskStatus.FINISHED:
            raise Exception(
                "Cannot save the results yet because task is not finished")
        with open(filePath, "w") as f:
            print(self.currentResponse.results, file=f)
