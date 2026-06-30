import os
from pathlib import Path
from typing import List, Dict

from langchain_ollama import OllamaEmbeddings
import chromadb

def load_faq_docs(data_dir: str = "data") -> List[Dict]:
    """
    Load all Markdown FAQ files from the specified directory.
    Each document is represented as a dict with page_content and metadata.
    """
    docs = []
    for md_file in Path(data_dir).glob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        docs.append(
            {
                "page_content": text,
                "metadata": {"source": md_file.name},
            }
        )
    return docs

def create_vector_store(docs: List[Dict], persist_dir: str = "chroma_faq") -> chromadb.Collection:
    """
    Create or load a persistent Chroma collection and add the provided documents.
    """
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name="faq")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    texts = [doc["page_content"] for doc in docs]
    metadatas = [doc["metadata"] for doc in docs]
    ids = [f"doc_{i}" for i in range(len(docs))]
    # Compute embeddings once
    doc_embeddings = embeddings.embed_documents(texts)
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=doc_embeddings,
    )
    return collection

def search_course_docs(collection: chromadb.Collection, query: str, k: int = 3) -> List[Dict]:
    """
    Query the collection for the top k relevant documents.
    """
    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas"],
    )
    docs = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        docs.append({"page_content": doc, "metadata": meta})
    return docs
