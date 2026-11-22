import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from src.supabase_client import supabase


# Load environment variables
load_dotenv()


# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Custom Supabase Retriever
class SupabaseRetriever:

    def __init__(self, k=5):
        self.k = k

    def invoke(self, query):

        # Generate query embedding
        query_embedding = embeddings.embed_query(query)

        # Retrieve only FactoryOps documents
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": self.k,
                "filter": {
                    "corpus": "factoryops"
                }
            }
        ).execute()

        documents = []

        for item in response.data or []:
            documents.append(
                Document(
                    page_content=item["content"],
                    metadata={
                        **(item.get("metadata") or {}),
                        "similarity": item["similarity"],
                        "id": item["id"]
                    }
                )
            )

        return documents


# Create retriever
retriever = SupabaseRetriever(k=5)


# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)