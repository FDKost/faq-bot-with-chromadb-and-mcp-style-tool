import os
from pathlib import Path
from typing import List, Dict

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.docstore.document import Document

def load_data_to_qdrant(
    data_dir: str,
    collection_name: str,
    qdrant_url: str,
    qdrant_api_key: str,
) -> Qdrant:
    """
    Load markdown files from the data directory, chunk them,
    and store them in a persistent Qdrant vector store.
    """
    data_path = Path(data_dir)
    md_files = list(data_path.glob("*.md"))
    documents: List[Document] = []
    for file_path in md_files:
        loader = TextLoader(str(file_path))
        docs = loader.load()
        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    vector_store = Qdrant.from_documents(
        texts,
        embeddings,
        client=client,
        collection_name=collection_name,
    )
    return vector_store


def get_qdrant_vector_store(
    collection_name: str,
    qdrant_url: str,
    qdrant_api_key: str,
) -> Qdrant:
    """
    Return an existing Qdrant vector store instance for later use.
    """
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    vector_store = Qdrant(client=client, collection_name=collection_name)
    return vector_store


def search_qdrant(
    vector_store: Qdrant,
    query: str,
    k: int = 5,
) -> List[Document]:
    """
    Perform a similarity search on the Qdrant collection and return the top‑k documents.
    """
    results = vector_store.similarity_search(query, k=k)
    return results
