# vector_db.py

import streamlit as st
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
class VectorStore:
    def __init__(self, text_chunks):
        self.text_chunks = text_chunks
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def build_faiss_index(self):
        """Create and return a FAISS index from text chunks."""
        with st.spinner("🔍 Creating semantic vector index..."):
            return FAISS.from_documents(self.text_chunks, self.embeddings)
