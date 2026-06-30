import os
from pathlib import Path
from typing import List, Dict

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def load_faq_to_chroma(
    data_dir: str,
    persist_directory: str = "./chroma_faq",
) -> Chroma:
    """
    Load all Markdown FAQ files in `data_dir` into a ChromaDB collection.
    The function chunks the files, generates embeddings using the
    `nomic-embed-text` Ollama model, and persists them in ChromaDB.

    Parameters
    ----------
    data_dir : str
        Path to the directory containing .md files.
    persist_directory : str, optional
        Directory where ChromaDB will store its data. Defaults to "./chroma_faq".

    Returns
    -------
    Chroma
        A vector store instance that can be used for similarity search.
    """
    # Ensure persistence directory exists
    os.makedirs(persist_directory, exist_ok=True)

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

    # Persist to ChromaDB
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    return vector_store


def search_course_docs(
    vector_store: Chroma,
    query: str,
    k: int = 3,
) -> List[Dict]:
    """
    Search the ChromaDB collection for the most relevant documents.

    Parameters
    ----------
    vector_store : Chroma
        The vector store instance created by `load_faq_to_chroma`.
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
