from enum import Enum

import streamlit as st
from langchain_core.documents.base import Document

from tax_bot.data import Message
from tax_bot.store import Store


class StateManager:
    class Key(str, Enum):
        MESSAGES = "messages"
        STORE = "store"
        DOCUMENTS = "documents"

    def __init__(self):
        if self.Key.MESSAGES not in st.session_state:
            st.session_state[self.Key.MESSAGES] = []
            st.session_state[self.Key.STORE] = Store()
            st.session_state[self.Key.DOCUMENTS] = []

    @property
    def messages(self) -> list[Message]:
        return st.session_state[self.Key.MESSAGES]

    @property
    def store(self) -> Store:
        return st.session_state[self.Key.STORE]

    @property
    def documents(self) -> list[Document]:
        return st.session_state[self.Key.DOCUMENTS]

    @documents.setter
    def documents(self, documents: list[Document]) -> None:
        st.session_state[self.Key.DOCUMENTS] = documents

    def add_message(self, message: Message):
        self.messages.append(message)

    def add_documents(self, documents: list[Document]) -> list[str]:
        return self.store.add_documents(documents)

    def clear(self):
        del st.session_state[self.Key.MESSAGES]
