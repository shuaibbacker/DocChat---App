# DocChat: Interactive Document Chat Application

**DocChat** is an interactive web application that allows users to upload PDF documents and engage in natural language conversations about their content. Built with Streamlit, this application leverages the power of large language models (LLMs) like Google's Gemini 1.5 Flash to provide intelligent, context-aware responses.

## Key Features

- **Interactive Chat Interface**: A user-friendly, chat-based interface for seamless interaction with your documents.
- **PDF Document Support**: Upload and process PDF files to make them ready for querying.
- **Advanced Language Models**: Utilizes state-of-the-art LLMs to understand and respond to a wide range of queries.
- **Efficient Indexing**: Employs FAISS for efficient similarity search, ensuring quick and relevant responses.
- **Modular and Extensible**: The codebase is organized into distinct modules for easy maintenance and future enhancements.

## How It Works

1. **Document Upload**: Users upload a PDF document through the Streamlit interface.
2. **Text Extraction and Chunking**: The application extracts text from the PDF and splits it into manageable chunks.
3. **Vectorization and Indexing**: The text chunks are converted into vector embeddings and stored in a FAISS index for fast retrieval.
4. **Question Answering**: When a user asks a question, the application retrieves the most relevant text chunks from the document and uses a Gemini-powered QA chain to generate a coherent and accurate answer.

## Core Components

- **`main.py`**: The entry point of the application, responsible for launching the Streamlit UI.
- **`streamlit_UI.py`**: Defines the user interface, including file uploads, chat history, and user input handling.
- **`pdf_upload.py`**: Manages the processing of uploaded PDF files, including text extraction and splitting.
- **`vector_db.py`**: Handles the creation of vector embeddings and the construction of the FAISS index.
- **`qa_retrieval.py`**: Implements the question-answering logic using a `RetrievalQA` chain and the Gemini 1.5 Flash model.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shuaibbacker/DocChat---App.git
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your environment**:
   - Create a `.env` file in the root directory.
   - Add your Google API key to the `.env` file:
     ```
     GOOGLE_API_KEY="YOUR_API_KEY"
     ```
4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## Future Enhancements

- Support for additional document formats (e.g., DOCX, TXT).
- Integration with other LLMs and embedding models.
- Enhanced chat features, such as conversation history and context management.

---

Feel free to contribute to the project by submitting pull requests or opening issues.
