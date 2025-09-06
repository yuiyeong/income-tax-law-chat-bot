from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_ollama import OllamaEmbeddings


class Store:
    MODEL_EMBEDDING_FUNCTION = "nomic-embed-text:v1.5"
    COLLECTION_NAME = "korean-income-tax"

    def __init__(self, persist_directory: str | None = None):
        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=OllamaEmbeddings(model=self.MODEL_EMBEDDING_FUNCTION),
            collection_name=self.COLLECTION_NAME,
        )

    def add_documents(self, documents: list[Document]) -> list[str]:
        return self.db.add_documents(documents)

    def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        return self.db.as_retriever(**kwargs)
