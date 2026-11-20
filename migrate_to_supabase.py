from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.supabase_client import supabase

load_dotenv()

# 1. Load the existing FAISS database
vectorstore = FAISS.load_local(
    "vectorstore",
    HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ),
    allow_dangerous_deserialization=True
)

# 2. Extract existing document chunks
documents = list(vectorstore.docstore._dict.values())

print(f"Total document chunks found: {len(documents)}")

if not documents:
    raise ValueError("No documents found in FAISS.")

# 3. Prevent accidental duplicate migration
existing = (
    supabase.table("rag_documents")
    .select("id")
    .limit(1)
    .execute()
)

if existing.data:
    raise RuntimeError(
        "Supabase already contains documents. "
        "Migration stopped to prevent duplicates."
    )

# 4. Generate embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [doc.page_content for doc in documents]

vectors = embeddings.embed_documents(texts)

# 5. Prepare Supabase records
records = []

for doc, vector in zip(documents, vectors):
    records.append({
        "content": doc.page_content,
        "metadata": doc.metadata,
        "embedding": vector
    })

# 6. Insert records in batches
batch_size = 50

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]

    response = (
        supabase.table("rag_documents")
        .insert(batch)
        .execute()
    )

    print(f"Uploaded {len(response.data)} chunks.")

print("Migration completed successfully!")
print(f"Total chunks migrated: {len(records)}")