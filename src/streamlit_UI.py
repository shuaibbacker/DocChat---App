import streamlit as st
from src.database import DatabaseLoader
from src.vector_db import VectorStore
from src.qa_retrieval import GeminiQABot

class StreamlitApp:
    def __init__(self):
        st.set_page_config(page_title="SQL-Chat App")
        st.title("📄 SQL-Chat App")

    def run(self):
        # Sidebar for DB connection
        with st.sidebar:
            st.header("Database Connection")
            db_host = st.text_input("Host")
            db_user = st.text_input("User")
            db_password = st.text_input("Password", type="password")
            db_name = st.text_input("Database")

            if st.button("Connect"):
                with st.spinner("Processing..."):
                    db_loader = DatabaseLoader(
                        host=db_host,
                        user=db_user,
                        password=db_password,
                        database=db_name
                    )
                    documents = db_loader.load_documents()
                    
                    vector_handler = VectorStore(documents)
                    docsearch = vector_handler.build_faiss_index()

                    st.session_state.qa_bot = GeminiQABot(docsearch)
                    st.success("✅ Database processed.")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            if "qa_bot" in st.session_state:
                with st.spinner("Getting response..."):
                    result = st.session_state.qa_bot.ask(prompt)
                    response = result["result"]
                    # Display assistant response in chat message container
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.warning("Please connect to the database first.")
