import os
from pathlib import Path
from typing import List, Dict

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


def load_faq_to_qdrant(
    data_dir: str,
    collection_name: str,
    host: str = "localhost",
    port: int = 6333,
) -> QdrantVectorStore:
    """
    Load all Markdown FAQ files in `data_dir` into a Qdrant collection.
    The function chunks the files, generates embeddings using the
    `nomic-embed-text` Ollama model, and persists them in Qdrant.

    Parameters
    ----------
    data_dir : str
        Path to the directory containing .md files.
    collection_name : str
        Name of the Qdrant collection to create or use.
    host : str, optional
        Qdrant host address. Defaults to "localhost".
    port : int, optional
        Qdrant port. Defaults to 6333.

    Returns
    -------
    QdrantVectorStore
        A vector store instance that can be used for similarity search.
    """
    # Initialize Qdrant client
    client = QdrantClient(host=host, port=port)

    # Read and chunk all markdown files
    texts: List[str] = []
    for md_file in Path(data_dir).glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_text(content)
        texts.extend(chunks)

    # Create embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Persist to Qdrant
    vector_store = QdrantVectorStore.from_texts(
        texts=texts,
        embedding=embeddings,
        collection_name=collection_name,
        client=client,
    )
    return vector_store


def search_course_docs(
    vector_store: QdrantVectorStore,
    query: str,
    k: int = 3,
) -> List[Dict]:
    """
    Search the Qdrant collection for the most relevant documents.

    Parameters
    ----------
    vector_store : QdrantVectorStore
        The vector store instance created by `load_faq_to_qdrant`.
    query : str
        The search query.
    k : int, optional
        Number of top results to return. Defaults to 3.

    Returns
    -------
    List[Dict]
        A list of dictionaries with a single key `page_content` containing
        the matched text.
    """
    docs = vector_store.similarity_search(query, k=k)
    return [{"page_content": doc.page_content} for doc in docs]
