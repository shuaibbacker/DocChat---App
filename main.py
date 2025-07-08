import os
import streamlit as st
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline

from transformers import pipeline

# Load environment variables (optional if you still use HF tokens)
load_dotenv()

st.title("📄 DocChat")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load PDF
    loader = PyPDFLoader("temp_uploaded.pdf")
    documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create FAISS vector store
    docsearch = FAISS.from_documents(text_chunks, embeddings)

    # Load transformers pipeline locally
    local_pipeline = pipeline("text2text-generation", model="google/flan-t5-large", max_length=512)

    # Wrap with LangChain
    llm = HuggingFacePipeline(pipeline=local_pipeline)

    # Build RetrievalQA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True
    )

    # User question input
    user_input = st.text_input("What is your question?")
    if user_input:
        result = qa.invoke({"query": user_input})
        st.write("🔎 **Response:**", result["result"])
