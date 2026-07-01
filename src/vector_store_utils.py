import os
from pathlib import Path
from typing import List, Dict, Any

from chromadb import Client
from chromadb import Collection
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
COLLECTION_NAME = "faq_collection"
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 1024  # Adjust if the model changes
CHROMA_PATH = "./chroma_faq"

def load_faq_to_chroma() -> Collection:
    """
    Load all markdown files from the data/ directory, split them into chunks,
    embed them, and store them in a Chroma collection.
    Returns the Chroma Collection instance.
    """
    # Initialize Chroma client with persistence
    client = Client(path=CHROMA_PATH)

    # Create or get collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Prepare text splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # Prepare embeddings
    embedder = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # Load markdown files
    data_dir = Path("data")
    docs = []
    ids = []
    metadatas = []

    for md_file in data_dir.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)
        for idx, chunk in enumerate(chunks):
            docs.append(chunk)
            ids.append(f"{md_file.stem}_{idx}")
            metadatas.append({"source": md_file.name})

    # Embed documents
    embeddings = embedder.embed_documents(docs)

    # Add to collection
    collection.add(
        documents=docs,
        ids=ids,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return collection

def search_course_docs(collection: Collection, query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Query the Chroma collection for the top k documents matching the query.
    Returns a list of dicts with page_content and score.
    """
    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "distances", "metadatas"],
    )
    docs = []
    for doc, distance, metadata in zip(
        results["documents"][0], results["distances"][0], results["metadatas"][0]
    ):
        docs.append(
            {
                "page_content": doc,
                "score": 1 - distance,  # Convert distance to similarity
                "metadata": metadata,
            }
        )
    return docs
