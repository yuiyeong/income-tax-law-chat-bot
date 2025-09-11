from langchain_core.documents.base import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_ollama import ChatOllama

from tax_bot.chains import Chains


class TaxAgent:
    CHAT_MODEL_NAME = "gpt-oss:20b"

    def __init__(self, documents: list[Document], retriever: VectorStoreRetriever):
        self.documents = documents
        self.retriever = retriever
        self.llm = ChatOllama(model=self.CHAT_MODEL_NAME)
        self.chains = Chains(self.llm, self.retriever)

    def query(self, query: str) -> str:
        chain = self.chains.get_dictionary_chain() | {"input": RunnablePassthrough()} | self.chains.get_tax_rag_chain()
        return chain.invoke(query, config={"configurable": {"session_id": "12312992"}})
