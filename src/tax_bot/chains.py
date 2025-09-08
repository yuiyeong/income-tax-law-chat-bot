from langchain import hub
from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.vectorstores.base import VectorStoreRetriever


class Chains:
    def __init__(self, llm: BaseChatModel, retriever: VectorStoreRetriever):
        self.llm = llm
        self.retriever = retriever
        self.str_parser = StrOutputParser()
        self.qna_prompt = hub.pull("rlm/rag-prompt")

    def get_dictionary_chain(self) -> RunnableSerializable:
        dictionary = ["사람을 나타내는 표현 -> 거주자"]
        dictionary_prompt = ChatPromptTemplate.from_template(f"""사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경하세요.
        만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        사전: {dictionary}
        질문: {{query}}""")
        return dictionary_prompt | self.llm | self.str_parser

    def get_tax_qna_chain(self) -> RunnableSerializable:
        qna_chain = (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | self.qna_prompt
            | self.llm
            | self.str_parser
        )
        return self.get_dictionary_chain() | qna_chain

    @staticmethod
    def _format_docs(docs: list[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)
