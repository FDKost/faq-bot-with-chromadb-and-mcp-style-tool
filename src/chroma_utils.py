import os
from pathlib import Path
from typing import List, Dict

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

CHROMA_DIR = Path(__file__).parent.parent / "chroma_faq"

def load_faq_to_chroma() -> Chroma:
    """
    Load markdown files from the data directory, chunk them,
    and store them in a persistent Chroma vector store.
    """
    data_dir = Path(__file__).parent.parent / "data"
    md_files = list(data_dir.glob("*.md"))
    documents = []
    for file_path in md_files:
        loader = TextLoader(str(file_path))
        docs = loader.load()
        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(documents)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create or load the Chroma store
    chroma = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    chroma.persist()
    return chroma

def search_course_docs(query: str, k: int = 3) -> List[Dict]:
    """
    Query the Chroma vector store and return the top k results.
    Each result is a dict with 'content' and 'metadata'.
    """
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    chroma = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )
    results = chroma.similarity_search(query, k=k)
    return [{"content": r.page_content, "metadata": r.metadata} for r in results]
