import os
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredFileLoader

from strategy_ai.ai_core.document_loaders.website import load_weblinks
from strategy_ai.ai_core.document_loaders.pptx import load_pptx
from strategy_ai.ai_core.document_loaders.xlsx import load_xlsx


class DocumentSource():
    def __init__(self, name: str, directory_path: str | None = None, filePaths: List[str] | None = None):
        self.name = name
        self.path = directory_path
        self.filePaths = filePaths
        self.documents = []
        if directory_path is not None:
            self.documents.extend(
                DocumentSource.documents_from_directory(directory_path))
        if filePaths is not None:
            self.documents.extend(
                DocumentSource.documents_from_files(filePaths))

    def documents_from_directory(directoryPath: str):
        """
        given a directory path (a folder), returns the documents in a format
        that can be interfaced with langchain.
        """
        documents = []
        for filename in os.listdir(directoryPath):
            file_path = os.path.join(directoryPath, filename)
            documents.extend(DocumentSource.file_load_documents(file_path))

        return documents
        # return DirectoryLoader(
        # path = directoryPath, # str
        # glob = "**/[!.]*", # str
        # silent_errors = True, # bool
        # load_hidden = False, # bool
        # loader_cls = UnstructuredFileLoader, # FILE_LOADER_TYPE
        # loader_kwargs = {"mode":"elements"}, # Union[dict, None] - elements mode gives file metadata
        # recursive = True, # bool
        # show_progress = True, # bool
        # use_multithreading = False, # bool
        # max_concurrency = 4, # int
        # ).load()

    def documents_from_files(file_paths: List[str]):
        """
        given a list of file paths, returns the documents in a format
        that can be interfaced with langchain.
        """
        documents = []
        for file_path in file_paths:
            documents.extend(DocumentSource.file_load_documents(file_path))

        return documents

    def file_load_documents(file_path: str):
        if file_path.endswith("weblinks.txt"):
            return load_weblinks(file_path)
        if file_path.endswith(".xlsx"):
            return load_xlsx(file_path)
        elif file_path.endswith(".pptx"):
            return load_pptx(file_path)
        else:
            docs = UnstructuredFileLoader(
                # Union[str, List[str]] - elements mode gives file metadata
                file_path=file_path,
                mode="paged",  # single, elements, paged
                unstructured_kwargs=None,  # Any
            ).load()
            for doc in docs:
                doc.metadata["text_format"] = "text"
            return docs

    def update_documents(newDocuments: list[Document]):
        """Given some new or updated documents, add them to this DocumentSource and remove the old copies
        """
        pass
