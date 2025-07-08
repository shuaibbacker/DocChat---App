# pdf_upload.py

import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
class PDFProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_and_split(self, chunk_size: int = 500, chunk_overlap: int = 20):
        """Load the PDF and split it into text chunks."""
        with st.spinner("📄 Reading and splitting the document..."):
            loader = PyPDFLoader(self.file_path)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            return text_splitter.split_documents(documents)
