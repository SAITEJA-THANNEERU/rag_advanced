# 🤖 Advanced Conversational RAG Chatbot

An AI-powered conversational chatbot built using **Retrieval-Augmented Generation (RAG)**, LangChain, FastAPI, Streamlit, Supabase, and Groq.

The application allows users to ask questions about company policy documents and receive context-aware answers using semantic search and Large Language Models.

## 🚀 Live Application

**Access the Chatbot:**

[Advanced RAG Chatbot – Live Demo](https://ragadvanced-production-4054751c.up.railway.app/)

**Backend API Documentation:**

[FastAPI Swagger Documentation](https://ragadvanced-production.up.railway.app/docs)

## 📌 Project Overview

Traditional chatbots often generate answers without referring to specific organizational documents.

This project addresses that limitation using Retrieval-Augmented Generation (RAG).

The system retrieves relevant information from uploaded company policy documents using vector similarity search and passes the retrieved context to an LLM to generate accurate, relevant responses.

It also supports conversational interactions by maintaining session-based chat history.

## ✨ Features

- **Conversational Chat Interface:** Interactive chatbot built with Streamlit.
- **Retrieval-Augmented Generation:** Generates answers using relevant document context.
- **Semantic Search:** Retrieves relevant document chunks using vector embeddings.
- **Supabase Vector Database:** Stores and retrieves document embeddings using pgvector.
- **LLM Integration:** Uses Groq-powered language models for response generation.
- **Conversation Memory:** Maintains chat history using session IDs.
- **Intent Detection:** Routes questions into document-related, conversation-history, and general-query categories.
- **REST API:** FastAPI backend for frontend and external application integration.
- **Cloud Deployment:** Frontend and backend deployed independently using Railway.
- **Dark UI:** Clean chatbot interface with dark theme support.

## 🏗️ System Architecture

```text
                 USER
                   |
                   v
            STREAMLIT FRONTEND
              (Chat Interface)
                   |
                   | HTTP Requests
                   v
              FASTAPI BACKEND
                (REST API)
                   |
                   v
              RAG PIPELINE
                   |
          +--------+---------+
          |        |         |
          v        v         v
       EMBEDDING  SUPABASE   GROQ
        MODEL     VECTOR     LLM
                  SEARCH
          |        |
          +--------+
                   |
                   v
             GENERATED ANSWER
                   |
                   v
            STREAMLIT FRONTEND
```

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Framework | LangChain |
| LLM Provider | Groq |
| Embedding Model | Sentence Transformers |
| Embedding Model Name | all-MiniLM-L6-v2 |
| Vector Database | Supabase (PostgreSQL + pgvector) |
| API Communication | REST API |
| Deployment | Railway |
| Environment Management | Python dotenv |

## 🔍 How It Works

1. The user enters a question through the Streamlit chatbot.
2. The frontend sends the question and session ID to the FastAPI backend.
3. The RAG pipeline identifies the query intent.
4. For document-related questions, the embedding model converts the question into a vector.
5. Supabase performs similarity search to retrieve relevant document chunks.
6. The retrieved context is passed to the Groq language model.
7. The LLM generates a context-aware response.
8. FastAPI returns the answer to Streamlit.
9. The chatbot displays the response and maintains conversation history.

## 📂 Project Structure

```text
rag_advanced/
│
├── app.py                    # Streamlit frontend
├── api.py                    # FastAPI backend
├── requirements.txt          # Project dependencies
├── migrate_to_supabase.py    # FAISS to Supabase migration
├── .env                      # Environment variables (not committed)
├── .gitignore
│
├── .streamlit/
│   └── config.toml            # Streamlit dark theme
│
├── data/
│   └── company_policy.pdf     # Knowledge base document
│
├── src/
│   ├── config.py              # LLM, embeddings and retriever
│   ├── chains.py              # LangChain chains
│   ├── prompts.py             # Prompt templates
│   ├── rag_pipeline.py        # Main RAG pipeline
│   └── supabase_client.py    # Supabase connection
│
└── vectorstore/               # Original FAISS backup
```

## ⚙️ Installation and Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SAITEJA-THANNEERU/rag_advanced.git
```

```bash
cd rag_advanced
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Add the following variables:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

RAG_API_URL=http://127.0.0.1:8000
```

Replace the placeholder values with your own credentials.

**Important:** Never commit your `.env` file or expose your service-role key.

### 5. Start the FastAPI Backend

Open a terminal and execute:

```bash
uvicorn api:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and execute:

```bash
streamlit run app.py
```

Frontend runs at:

```text
http://localhost:8501
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Backend health check |
| POST | `/chat` | Submit a question and receive an answer |
| DELETE | `/clear-history/{session_id}` | Clear conversation history |

### Chat API Example

**Request:**

```json
{
  "session_id": "test-session-001",
  "question": "What is the leave policy?"
}
```

**Response:**

```json
{
  "session_id": "test-session-001",
  "question": "What is the leave policy?",
  "answer": "The company provides Casual Leave, Sick Leave, and Earned Leave according to its leave policy."
}
```

## ☁️ Deployment

The application is deployed using Railway with two independent services.

| Service | Technology | Responsibility |
|---|---|---|
| Frontend | Streamlit | Chat interface |
| Backend | FastAPI | RAG processing and API services |

The frontend communicates with the backend through HTTP requests.

Environment variables and API credentials are configured separately in the deployment environment.

## 🔮 Future Enhancements

- Role-Based Retrieval-Augmented Generation (Role-Based RAG).
- User authentication and authorization.
- Organization-specific document access.
- Source citations and document references in responses.
- Persistent conversation history.
- Multiple document formats and knowledge bases.
- Integration with the FactoryOps application.
- Advanced agentic RAG workflows.
- Document upload and management interface.

## 🎯 Project Objective

The primary objective is to develop a modular, scalable, and reusable RAG-based conversational AI system that can retrieve organizational knowledge and generate context-aware responses.

The backend is designed to support future integration with enterprise applications such as FactoryOps, including role-based access to organizational information.

## 👨‍💻 Author

**Sai Teja Thanneeru**

Software Engineer | AI & Backend | Full Stack Developer

[GitHub](https://github.com/SAITEJA-THANNEERU)

[Portfolio](https://saiteja-portfolio-mikey.vercel.app/)

---

⭐ If you find this project interesting, consider giving the repository a star!
