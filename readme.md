# 📄 AI PDF Research Assistant

An AI-powered PDF Question Answering application built using **Retrieval-Augmented Generation (RAG)**. Upload PDF documents, ask natural language questions, and receive context-aware answers generated using Large Language Models (LLMs).

> Developed as a full-stack AI application using React, FastAPI, FAISS, HuggingFace Embeddings, and Groq LLMs.

---

## 🚀 Features

- 📂 Upload PDF documents
- 💬 Ask natural language questions about uploaded PDFs
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search using vector embeddings
- ⚡ FastAPI backend with REST APIs
- 🎨 Modern React frontend
- 📚 Document chunking for better retrieval
- 🤖 AI-generated answers powered by Groq
- 📌 Multiple document support (work in progress)
- 🌙 Clean dark-themed user interface

---

## 🏗️ Tech Stack

### Frontend

- React
- Vite
- CSS

### Backend

- FastAPI
- Python

### AI / Machine Learning

- LangChain
- FAISS
- HuggingFace Embeddings
- Sentence Transformers
- Groq LLM
- Retrieval-Augmented Generation (RAG)

### Libraries

- PyMuPDF
- pypdf
- python-dotenv

### Tools

- Git
- GitHub
- VS Code

---

# 📂 Project Structure

```
Ai-Pdf-Assistant
│
├── backend
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── uploads/
│   ├── vector_store/
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

# ⚙️ How It Works

1. User uploads a PDF document.
2. Text is extracted from the uploaded PDF.
3. The document is split into smaller semantic chunks.
4. HuggingFace Embeddings convert each chunk into vector representations.
5. FAISS stores and indexes the vectors.
6. User asks a question.
7. Relevant chunks are retrieved using similarity search.
8. Retrieved context is sent to the Groq LLM.
9. The LLM generates an accurate answer based on the retrieved content.

---

# 🧠 RAG Pipeline

```
                PDF
                 │
                 ▼
        Text Extraction
                 │
                 ▼
         Document Chunking
                 │
                 ▼
    HuggingFace Embeddings
                 │
                 ▼
         FAISS Vector Store
                 │
                 ▼
          Similarity Search
                 │
                 ▼
        Relevant Context
                 │
                 ▼
             Groq LLM
                 │
                 ▼
          Final Response
```

---

# 📸 Screenshots

## Home Page

> *(Add screenshot here)*

---

## Upload PDF

> *(Add screenshot here)*

---

## Ask Questions

> *(Add screenshot here)*

---

## AI Response

> *(Add screenshot here)*

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/T-A-R-01/Ai-Pdf-Assistant.git
```

Move into the project

```bash
cd Ai-Pdf-Assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
cd backend
uvicorn main:app --reload
```

---

# ▶️ Run Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 🎯 Future Improvements

- Multi-document conversations
- Conversation history
- User authentication
- Cloud deployment
- Citation-aware responses
- Streaming responses
- Drag-and-drop PDF upload
- Better document management
- Markdown rendering
- Docker support

---

# 📚 Learning Outcomes

This project helped me gain hands-on experience with:

- Retrieval-Augmented Generation (RAG)
- Vector Databases (FAISS)
- Semantic Search
- FastAPI Backend Development
- React Frontend Development
- REST API Integration
- Prompt Engineering
- Embedding Models
- Full Stack AI Application Development
- Git & GitHub Workflow

---

# 👨‍💻 Author

**Tushar Rai**

📍 Mumbai, India

GitHub

https://github.com/T-A-R-01

LinkedIn

https://www.linkedin.com/in/tushar-rai-7b8b792b8/

---

# ⭐ If you found this project useful, consider giving it a star!
