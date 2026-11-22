from src.config import retriever

from langchain_core.runnables import RunnableLambda

from src.chains import (
    contextualize_chain,
    document_answer_chain,
    intent_chain,
    history_answer_chain,
    general_chain
)


# ==========================================
# DOCUMENT RETRIEVAL
# ==========================================

def retrieve_documents(inputs):

    # 1. Rewrite the question using chat history
    standalone_question = contextualize_chain.invoke(
        {
            "input": inputs["input"],
            "chat_history": inputs["chat_history"]
        }
    )

    print("\nRewritten Question:", standalone_question)

    # 2. Retrieve relevant FactoryOps documents
    documents = retriever.invoke(standalone_question)

    print("\nRetrieved Documents:", len(documents))

    # 3. Handle empty retrieval
    if not documents:
        return (
            "I couldn't find relevant information in the "
            "FactoryOps knowledge base to answer this question."
        )

    # 4. Build context
    context = "\n\n".join(
        [
            f"""
            Source: {doc.metadata.get('source', 'Unknown')}
            Content:
            {doc.page_content}
            """
            for doc in documents
        ]
    )

    # 5. Generate grounded answer
    answer = document_answer_chain.invoke(
        {
            "input": standalone_question,
            "context": context
        }
    )

    return answer


# ==========================================
# QUERY ROUTING
# ==========================================

def route_request(inputs):

    question = inputs["input"]
    history = inputs.get("chat_history", [])

    # 1. Identify user intent
    intent = intent_chain.invoke(
        {
            "input": question,
            "chat_history": history
        }
    ).strip().upper()

    print("\nDetected Intent:", intent)

    # 2. Route document-related questions
    if intent == "DOCUMENT":

        return retrieve_documents(
            {
                "input": question,
                "chat_history": history
            }
        )

    # 3. Route conversation-history questions
    elif intent == "HISTORY":

        return history_answer_chain.invoke(
            {
                "input": question,
                "chat_history": history
            }
        )

    # 4. Route general conversation
    elif intent == "GENERAL":

        return general_chain.invoke(
            {
                "input": question,
                "chat_history": history
            }
        )

    # 5. Fallback
    else:

        print("Unknown intent. Using general chain.")

        return general_chain.invoke(
            {
                "input": question,
                "chat_history": history
            }
        )


# ==========================================
# RAG CHAIN
# ==========================================

rag_chain = RunnableLambda(route_request)