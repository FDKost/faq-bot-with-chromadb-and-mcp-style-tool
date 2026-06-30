import os
from pathlib import Path
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.docstore.document import Document

def load_data_to_qdrant(
    data_dir: str,
    collection_name: str,
    qdrant_url: str,
    qdrant_api_key: str = None,
) -> QdrantVectorStore:
    """
    Load all .md files from `data_dir`, chunk them by double newline,
    embed them using the Ollama `nomic-embed-text` model, and store
    the embeddings in a Qdrant collection.
    """
    texts: List[str] = []
    for file_path in Path(data_dir).glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Simple chunking: split by double newline
            chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
            texts.extend(chunks)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    store = QdrantVectorStore.from_texts(
        texts,
        embeddings,
        collection_name=collection_name,
        url=qdrant_url,
        api_key=qdrant_api_key,
    )
    return store

def search_qdrant(
    vector_store: QdrantVectorStore,
    query: str,
    k: int = 3,
) -> List[Document]:
    """
    Perform a similarity search in the Qdrant collection.
    Returns a list of Documents with `page_content` containing the chunk text.
    """
    return vector_store.similarity_search(query, k=k)
