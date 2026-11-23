import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List

from langchain_core.messages import HumanMessage, AIMessage
from src.auth import verify_token
from src.rag_pipeline import rag_chain


app = FastAPI(
    title="FactoryOps Conversational RAG API",
    description="Authenticated FactoryOps RAG Backend",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Conversation history
store: Dict[str, List] = {}


class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.get("/")
def home():
    return {"message": "FactoryOps RAG API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(
    request: ChatRequest,
    user: dict = Depends(verify_token)
):
    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        if len(question) > 5000:
            raise HTTPException(
                status_code=400,
                detail="Question is too long"
            )

        # Isolate conversation history by authenticated user
        session_key = f"{user['user_id']}:{request.session_id}"

        if session_key not in store:
            store[session_key] = []

        chat_history = store[session_key]

        answer = rag_chain.invoke({
            "input": question,
            "chat_history": chat_history[-10:]
        })

        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=answer))

        return {
            "session_id": request.session_id,
            "question": question,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Error processing your question"
        )


@app.delete("/clear-history/{session_id}")
def clear_history(
    session_id: str,
    user: dict = Depends(verify_token)
):
    session_key = f"{user['user_id']}:{session_id}"

    store.pop(session_key, None)

    return {
        "message": "Chat history cleared successfully"
    }