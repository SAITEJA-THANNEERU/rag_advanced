import argparse
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_huggingface import HuggingFaceEmbeddings

from src.supabase_client import supabase


# =====================================================
# CONFIGURATION
# =====================================================

load_dotenv()

DATA_DIR = Path("data/factoryops")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

BATCH_SIZE = 50

CHUNK_SIZE = 1800
CHUNK_OVERLAP = 270

FACTORY_ID = "FAC-001"

ALLOWED_ROLES = [
    "SUPER_ADMIN",
    "ADMIN",
    "MANAGER_SUPERVISOR",
    "PRODUCTION_PLANNER",
    "TECHNICIAN",
]


# =====================================================
# INITIALIZE EMBEDDINGS
# =====================================================

print("Initializing embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# =====================================================
# MARKDOWN DOCUMENT LOADING
# =====================================================

def load_markdown_documents():

    files = sorted(DATA_DIR.glob("*.md"))

    if not files:
        raise FileNotFoundError(
            f"No Markdown documents found in {DATA_DIR}"
        )

    documents = []

    for file_path in files:

        content = file_path.read_text(
            encoding="utf-8"
        )

        if not content.strip():
            print(f"Skipping empty file: {file_path.name}")
            continue

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "doc_id": file_path.stem,
                    "corpus": "factoryops",
                    "factory_id": FACTORY_ID,
                }
            )
        )

        print(f"Loaded: {file_path.name}")

    print(f"\nTotal documents loaded: {len(documents)}")

    return documents


# =====================================================
# MARKDOWN HEADER-AWARE CHUNKING
# =====================================================

def split_documents(documents):

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "section"),
            ("##", "subsection"),
            ("###", "topic"),
        ],
        strip_headers=False,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
        add_start_index=True,
    )

    all_chunks = []

    for document in documents:

        sections = header_splitter.split_text(
            document.page_content
        )

        for section in sections:

            section_chunks = text_splitter.split_documents(
                [section]
            )

            for chunk in section_chunks:

                metadata = {
                    **document.metadata,
                    **chunk.metadata,
                }

                metadata.update({
                    "allowed_roles": ALLOWED_ROLES,
                    "verification_status": "SEE_SOURCE_DOCUMENT",
                    "safety_critical": (
                        "safety" in document.metadata["source"].lower()
                        or "safety" in str(
                            chunk.metadata.get("subsection", "")
                        ).lower()
                        or "safety" in str(
                            chunk.metadata.get("topic", "")
                        ).lower()
                    ),
                })

                chunk.metadata = metadata

                all_chunks.append(chunk)

    print(f"\nTotal chunks generated: {len(all_chunks)}")

    return all_chunks


# =====================================================
# CHECK EXISTING FACTORYOPS DOCUMENTS
# =====================================================

def get_existing_factoryops_ids():

    existing_ids = []

    start = 0
    page_size = 500

    while True:

        response = (
            supabase.table("rag_documents")
            .select("id, metadata")
            .range(start, start + page_size - 1)
            .execute()
        )

        rows = response.data or []

        for row in rows:

            metadata = row.get("metadata") or {}

            if metadata.get("corpus") == "factoryops":
                existing_ids.append(row["id"])

        if len(rows) < page_size:
            break

        start += page_size

    return existing_ids


# =====================================================
# UPLOAD TO SUPABASE
# =====================================================

def upload_chunks(chunks, replace=False):

    existing_ids = get_existing_factoryops_ids()

    if existing_ids and not replace:

        raise RuntimeError(
            f"Found {len(existing_ids)} existing FactoryOps chunks. "
            "Use --replace to replace them intentionally."
        )

    if existing_ids and replace:

        print(
            f"Replacing {len(existing_ids)} existing FactoryOps chunks..."
        )

        for i in range(0, len(existing_ids), BATCH_SIZE):

            batch_ids = existing_ids[i:i + BATCH_SIZE]

            (
                supabase.table("rag_documents")
                .delete()
                .in_("id", batch_ids)
                .execute()
            )

    uploaded = 0

    for i in range(0, len(chunks), BATCH_SIZE):

        batch = chunks[i:i + BATCH_SIZE]

        texts = [
            chunk.page_content
            for chunk in batch
        ]

        vectors = embeddings.embed_documents(texts)

        records = []

        for chunk, vector in zip(batch, vectors):

            records.append({
                "content": chunk.page_content,
                "metadata": chunk.metadata,
                "embedding": vector,
            })

        response = (
            supabase.table("rag_documents")
            .insert(records)
            .execute()
        )

        uploaded += len(response.data or [])

        print(
            f"Uploaded {uploaded}/{len(chunks)} chunks"
        )

    print("\nFactoryOps ingestion completed successfully!")

    print(f"Total chunks uploaded: {uploaded}")


# =====================================================
# MAIN
# =====================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace previously ingested FactoryOps documents."
    )

    args = parser.parse_args()

    print("\n====================================")
    print(" FACTORYOPS DOCUMENT INGESTION")
    print("====================================\n")

    documents = load_markdown_documents()

    chunks = split_documents(documents)

    upload_chunks(
        chunks,
        replace=args.replace
    )


if __name__ == "__main__":
    main()