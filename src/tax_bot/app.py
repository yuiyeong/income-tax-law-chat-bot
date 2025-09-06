from enum import Enum

import streamlit as st

from tax_bot.data import Message
from tax_bot.loader import IncomeTaxLawDocumentLoader
from tax_bot.state_manager import StateManager


class TaxBotApp:
    class ROLE(str, Enum):
        USER = "user"
        HUMAN = "human"
        AI = "ai"
        ASSISTANT = "assistant"

    def __init__(self):
        self.avatars = {
            self.ROLE.USER: "🧐",
            self.ROLE.HUMAN: "🧐",
            self.ROLE.AI: "🎓",
            self.ROLE.ASSISTANT: "🎓",
        }

    def render(self):
        st.set_page_config(
            page_title="소득세 챗봇",
            page_icon="💬",
            layout="wide",
        )

        st.title("💬 소득세 챗봇")
        st.subheader("소득세에 관련된 모든 것을 답해드립니다!")

        state_manager = StateManager()
        if not state_manager.documents:
            # 문서 먼저 loading
            with st.spinner("소득세법 로딩중..."):
                loader = IncomeTaxLawDocumentLoader.create_from_asset()
                state_manager.documents = loader.load_and_split()
                state_manager.store.add_documents(state_manager.documents)

        for message in state_manager.messages:
            with st.chat_message(message.role, avatar=self.avatars[message.role]):
                st.write(message.content)

        if user_question := st.chat_input(placeholder="소득세에 관해서 질문을 해주세요."):
            with st.chat_message(self.ROLE.USER, avatar=self.avatars[self.ROLE.USER]):
                st.write(user_question)

                state_manager.add_message(Message.from_user(user_question))
