
import os

from dotenv import load_dotenv
load_dotenv()

from typing import Dict, List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, AIMessage

from src.auth import verify_token
from src.rag_pipeline import rag_chain


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="FactoryOps Conversational RAG API",
    description="Authenticated FactoryOps RAG Backend",
    version="2.1.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# ==========================================
# CONVERSATION HISTORY
# ==========================================

store: Dict[str, List] = {}


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=5000)


# ==========================================
# HEALTH ENDPOINTS
# ==========================================

@app.get("/")
def home():
    return {
        "message": "FactoryOps RAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ==========================================
# AUTHENTICATED CHAT ENDPOINT
# ==========================================

@app.post("/chat")
def chat(
    request: ChatRequest,
    user: dict = Depends(verify_token)
):
    try:

        # ----------------------------------
        # 1. Validate question
        # ----------------------------------

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

        # ----------------------------------
        # 2. Validate authenticated identity
        # ----------------------------------

        user_id = user.get("user_id")
        role = user.get("role")
        factory_id = user.get("factory_id")

        if not user_id or not role:
            raise HTTPException(
                status_code=403,
                detail="Invalid authenticated user"
            )

        if role != "SUPER_ADMIN" and not factory_id:
            raise HTTPException(
                status_code=403,
                detail="Factory assignment required"
            )

        # ----------------------------------
        # 3. Isolate conversation by user
        # ----------------------------------

        session_key = f"{user_id}:{request.session_id}"

        if session_key not in store:
            store[session_key] = []

        chat_history = store[session_key]

        # ----------------------------------
        # 4. Pass authenticated identity
        #    into the RAG pipeline
        # ----------------------------------

        answer = rag_chain.invoke({

            "input": question,

            "chat_history": chat_history[-10:],

            "user": {
                "user_id": user_id,
                "role": role,
                "factory_id": factory_id
            }

        })

        # ----------------------------------
        # 5. Update conversation history
        # ----------------------------------

        chat_history.append(
            HumanMessage(content=question)
        )

        chat_history.append(
            AIMessage(content=answer)
        )

        # ----------------------------------
        # 6. Return response
        # ----------------------------------

        return {
            "session_id": request.session_id,
            "question": question,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:

        print("Error processing chat request:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Error processing your question"
        )


# ==========================================
# CLEAR CHAT HISTORY
# ==========================================

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
