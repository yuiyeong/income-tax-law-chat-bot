from enum import Enum

import streamlit as st

from tax_bot.data import Message


class StateManager:
    class Key(str, Enum):
        MESSAGES = "messages"

    def __init__(self):
        if self.Key.MESSAGES not in st.session_state:
            st.session_state[self.Key.MESSAGES] = []

    @property
    def messages(self) -> list[Message]:
        return st.session_state[self.Key.MESSAGES]

    def add_message(self, message: Message):
        self.messages.append(message)

    def clear(self):
        del st.session_state[self.Key.MESSAGES]
