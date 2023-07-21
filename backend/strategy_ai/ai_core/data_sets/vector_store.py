import os

from typing import Any

from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# more info on embeddings
# Here I am using OpenAI, there are many other options: https://python.langchain.com/docs/modules/data_connection/vectorstores/

# more info on vector stores
# https://api.python.langchain.com/en/latest/modules/vectorstores.html

# Here I'm using FAISS: https://faiss.ai/


class FAISSVectorStore():
    def __init__(self, splitDocuments, vectorStoreSavePath: str = ""):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",  # str
            deployment="text-embedding-ada-002",  # str
            openai_api_version="",  # str | None - this stuff has to do with priority access
            openai_api_base="",  # str | None - this stuff has to do with priority access
            openai_api_type="",  # str | None - this stuff has to do with priority access
            openai_proxy="",  # str | None - this stuff has to do with priority access
            embedding_ctx_length=8191,  # int
            openai_api_key=None,  # str | None - filled using the environment variable: OPENAI_API_KEY
            openai_organization=None,  # str | None
            allowed_special=set(),  # Set[str] | Literal['all']
            # Set[str] | Sequence[str] | Literal['all']
            disallowed_special="all",
            chunk_size=1000,  # int
            max_retries=6,  # int
            request_timeout=None,  # float | Tuple[float, float] | None
            headers=None,  # Any
        )
        self.splitDocuments = splitDocuments

        if vectorStoreSavePath == "":
            self.rebuild_from_documents(self.splitDocuments, self.embeddings)
        else:
            self.reload_from_save(vectorStoreSavePath)

    def rebuild_from_documents(self, splitDocuments: list[Document], embeddings) -> None:
        if type(splitDocuments) is not list and splitDocuments[0] is not Document:
            raise Exception(
                f"split documents are not valid, type: {type(splitDocuments)}[{type(splitDocuments[0])}]")

        self.vectorStore = FAISS.from_documents(
            splitDocuments, embeddings or self.embeddings)

    def reload_from_save(self, savePath: str) -> None:
        if os.path.exists(savePath):
            self.vectorStore = FAISS.load_local(
                savePath, self.embeddings)
        else:
            raise Exception(
                f"vector store save not found: {savePath}")

    def as_retriever(self):
        return self.vectorStore.as_retriever()

    def similarity_search_with_score(self, query: str, k: int = 4, filter: dict[str, Any] | None = None, fetch_k: int = 20):
        return self.vectorStore.similarity_search_with_score(query, k, filter, fetch_k)

    def search_result_markdown(searchResult, lineSeparator="\n"):
        """Given search results from a vectorstore, return the results formatted
        using the markdown format."""
        return f"""
        # Context Results:{lineSeparator}
        {lineSeparator.join([f'''
        ## Result No. {num}{lineSeparator}
        ### Source:{lineSeparator}{r[0].metadata.get('source')}, on page: {r[0].metadata.get('page_name')}{lineSeparator}
        #### Score (lower is better):{lineSeparator}{r[1]}{lineSeparator}
        #### Content:{lineSeparator}```{r[0].metadata.get("text_format")}{lineSeparator}{r[0].page_content}{lineSeparator}```
        '''
        for num, r in enumerate(searchResult, 1)
        ])}
        """

    def formatted_context(self, query: str, k: int = 4, filter: dict[str, Any] | None = None, fetch_k: int = 20):
        return FAISSVectorStore.search_result_markdown(self.similarity_search_with_score(query, k, filter, fetch_k))

    def save_to_local(self, savePath: str):
        if os.path.exists(savePath):
            self.vectorStore.save_local(savePath)
        else:
            raise Exception(f"save path invalid: {savePath}")
