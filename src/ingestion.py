import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_faq")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def load_faq_to_chroma(data_dir: str = "data", chroma_path: str = None) -> None:
    """
    Load all .md files from data_dir, chunk them, embed, and persist to ChromaDB.
    Avoid duplicating documents on subsequent runs.
    """
    if chroma_path is None:
        chroma_path = CHROMA_DB_PATH

    # Read all markdown files
    texts: List[str] = []
    metadata: List[dict] = []
    for md_file in Path(data_dir).glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            texts.append(content)
            metadata.append({"source_file": md_file.name})

    if not texts:
        raise ValueError(f"No markdown files found in {data_dir}")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(texts)
    chunk_metadata = []
    for i, chunk in enumerate(chunks):
        # Associate each chunk with its source file
        source_file = metadata[i // (len(texts) // len(chunks) + 1)]["source_file"]
        chunk_metadata.append({"source_file": source_file})

    # Initialize embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)

    # Load existing collection if present
    db = Chroma(persist_directory=chroma_path, embedding_function=embeddings)

    # Retrieve existing documents to avoid duplicates
    existing_docs = db.get()
    existing_texts = [doc.page_content for doc in existing_docs]

    # Filter out duplicates
    new_chunks = []
    new_metadata = []
    for chunk, meta in zip(chunks, chunk_metadata):
        if chunk not in existing_texts:
            new_chunks.append(chunk)
            new_metadata.append(meta)

    if new_chunks:
        db.add_texts(new_chunks, metadatas=new_metadata)
        db.persist()
        print(f"Persisted {len(new_chunks)} new chunks to ChromaDB at {chroma_path}")
    else:
        print("No new documents to add; ChromaDB is up to date.")

def search_course_docs(query: str, k: int = 3, chroma_path: str = None) -> List[str]:
    """
    Query the ChromaDB store and return the top k relevant snippets.
    """
    if chroma_path is None:
        chroma_path = CHROMA_DB_PATH

    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)
    db = Chroma(persist_directory=chroma_path, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in docs]
