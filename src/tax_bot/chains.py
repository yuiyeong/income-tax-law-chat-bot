from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.vectorstores.base import VectorStoreRetriever


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


class Chains:
    def __init__(self, llm: BaseChatModel, retriever: VectorStoreRetriever):
        self.llm = llm
        self.retriever = retriever
        self.str_parser = StrOutputParser()

    @property
    def dictionary_prompt(self) -> ChatPromptTemplate:
        dictionary = ["사람을 나타내는 표현 -> 거주자"]
        return ChatPromptTemplate.from_template(f"""사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경하세요.
                만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
                사전: {dictionary}
                질문: {{query}}""")

    @property
    def history_prompt(self) -> ChatPromptTemplate:
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        return ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    @property
    def qna_prompt(self) -> ChatPromptTemplate:
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    def get_dictionary_chain(self) -> RunnableSerializable:
        return self.dictionary_prompt | self.llm | self.str_parser

    def get_tax_rag_chain(self) -> RunnableSerializable:
        history_aware_retriever = create_history_aware_retriever(self.llm, self.retriever, prompt=self.history_prompt)
        question_answer_chain = create_stuff_documents_chain(self.llm, self.qna_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        return RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        ).pick("answer")

    @staticmethod
    def _format_docs(docs: list[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)
