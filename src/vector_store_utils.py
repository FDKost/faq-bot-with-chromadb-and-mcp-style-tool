import os
from pathlib import Path
from typing import List, Dict

from chromadb import PersistentClient
from langchain_ollama import OllamaEmbeddings

def load_data_to_chroma(
    data_dir: str,
    collection_name: str = "faq_collection",
    persist_dir: str = "./chroma_faq",
) -> PersistentClient:
    """
    Load all .md files from data_dir into a ChromaDB collection.
    The collection is persisted to persist_dir.
    """
    client = PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name=collection_name)

    # Use Ollama embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Prepare documents
    documents = []
    metadatas = []
    ids = []

    for md_file in Path(data_dir).glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Split into chunks by double newline
        chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({"source": md_file.name})
            ids.append(f"{md_file.stem}_{i}")

    if documents:
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    return collection

def search_course_docs(
    collection,
    query: str,
    k: int = 3,
) -> List[Dict]:
    """
    Query the ChromaDB collection and return the top k relevant documents.
    Each result is a dict with 'page_content' and 'metadata'.
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
