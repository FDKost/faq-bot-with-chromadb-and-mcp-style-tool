import os
import json
from pathlib import Path
from typing import List, Dict, Any

from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from langchain_community.vectorstores import Qdrant as LangchainQdrant

# Constants
COLLECTION_NAME = "faq_collection"
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 1024  # Adjust if the model changes

def load_faq_docs() -> List[Dict[str, Any]]:
    """
    Load all markdown files from the data/ directory, split them into chunks,
    and return a list of dicts with page_content and metadata.
    """
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    data_dir = Path("data")
    for md_file in data_dir.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)
        for chunk in chunks:
            docs.append(
                {
                    "page_content": chunk,
                    "metadata": {"source": md_file.name},
                }
            )
    return docs

def create_vector_store(docs: List[Dict[str, Any]]) -> QdrantClient:
    """
    Create a Qdrant collection and upsert the provided documents.
    Returns the QdrantClient instance.
    """
    client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"),
                          port=int(os.getenv("QDRANT_PORT", "6333")))
    # Create collection if it doesn't exist
    if COLLECTION_NAME not in client.get_collections().collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qdrant_models.VectorParams(
                size=EMBEDDING_DIM,
                distance=qdrant_models.Distance.COSINE,
            ),
        )
    # Prepare embeddings
    embedder = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectors = []
    for idx, doc in enumerate(docs):
        embedding = embedder.embed_query(doc["page_content"])
        vectors.append(
            qdrant_models.PointStruct(
                id=idx,
                vector=embedding,
                payload=doc["metadata"],
            )
        )
    # Upsert points
    client.upsert(collection_name=COLLECTION_NAME, points=vectors)
    return client

def get_vector_store(client: QdrantClient):
    """
    Return a LangChain Qdrant vector store wrapper for the collection.
    """
    return LangchainQdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=OllamaEmbeddings(model=EMBEDDING_MODEL),
    )

def search_course_docs(client: QdrantClient, query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Query the Qdrant collection for the top k documents matching the query.
    Returns a list of dicts with page_content and score.
    """
    embedder = OllamaEmbeddings(model=EMBEDDING_MODEL)
    query_vector = embedder.embed_query(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
    )
    docs = []
    for res in results:
        docs.append(
            {
                "page_content": res.payload.get("source", ""),
                "score": res.score,
                "metadata": res.payload,
            }
        )
    return docs
