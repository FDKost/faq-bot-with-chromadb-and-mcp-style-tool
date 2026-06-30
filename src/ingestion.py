import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def load_faq_to_chroma(data_dir: str = "data", chroma_path: str = "./chroma_faq") -> None:
    """
    Load all .md files from data_dir, chunk them, embed, and persist to ChromaDB.
    """
    texts: List[str] = []
    for md_file in Path(data_dir).glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            texts.append(f.read())

    if not texts:
        raise ValueError(f"No markdown files found in {data_dir}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_text(texts)

    embeddings = OpenAIEmbeddings()
    db = Chroma.from_texts(docs, embeddings, persist_directory=chroma_path)
    db.persist()
    print(f"Persisted {len(docs)} chunks to ChromaDB at {chroma_path}")

def search_course_docs(query: str, k: int = 3, chroma_path: str = "./chroma_faq") -> List[str]:
    """
    Query the ChromaDB store and return the top k relevant snippets.
    """
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=chroma_path, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in docs]
