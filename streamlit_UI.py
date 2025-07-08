# streamlit_UI.py

import os
import streamlit as st
from dotenv import load_dotenv
from pdf_upload import PDFProcessor
from vector_db import VectorStore
from qa_retrieval import GeminiQABot

class StreamlitApp:
    def __init__(self):
        st.set_page_config(page_title="📄 Doc ChatBot", page_icon="🤖")
        st.title("🤖 Doc ChatBot")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "qa_bot" not in st.session_state:
            st.session_state.qa_bot = None

    def upload_and_process_pdf(self):
        with st.sidebar:
            st.header("📂 Upload Document")
            uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

        if uploaded_file is not None:
            with st.spinner("⏳ Uploading and preparing..."):
                with open("temp_uploaded.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                processor = PDFProcessor("temp_uploaded.pdf")
                text_chunks = processor.load_and_split()

                vector_handler = VectorStore(text_chunks)
                docsearch = vector_handler.build_faiss_index()

                st.session_state.qa_bot = GeminiQABot(docsearch)
                st.session_state.chat_history = []

                st.success("✅ Document processed and ready to chat!")
                st.toast("Start chatting with your document!")

    def display_chat(self):
        for msg in st.session_state.chat_history:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(msg["user"])
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["bot"])

    def chat_input_and_reply(self):
        if st.session_state.qa_bot:
            user_input = st.chat_input("Ask me anything about your document...")

            if user_input:
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": "..."
                })
                st.rerun()

            if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "...":
                user_question = st.session_state.chat_history[-1]["user"]
                response = st.session_state.qa_bot.ask(user_question)
                st.session_state.chat_history[-1]["bot"] = response
                st.rerun()

    def run(self):
        st.markdown("🗂️ Upload a PDF and chat with it using **Gemini 1.5 Flash**.")
        self.upload_and_process_pdf()
        self.display_chat()
        self.chat_input_and_reply()
