import os
import shutil
import pytest
from pathlib import Path

from src.ingestion import load_faq_to_chroma, CHROMA_DB_PATH
from langchain_chroma import Chroma

@pytest.fixture(scope="module")
def chroma_dir(tmp_path_factory):
    # Use a temporary directory for ChromaDB
    path = tmp_path_factory.mktemp("chroma")
    return str(path)

def test_load_faq_to_chroma(chroma_dir):
    # Ensure clean state
    if os.path.exists(chroma_dir):
        shutil.rmtree(chroma_dir)

    # Load data
    load_faq_to_chroma(data_dir="data", chroma_path=chroma_dir)

    # Verify that the collection exists and has documents
    db = Chroma(persist_directory=chroma_dir, embedding_function=None)
    docs = db.get()
    assert len(docs) > 0, "ChromaDB should contain documents after ingestion"

    # Run again to ensure no duplicates
    load_faq_to_chroma(data_dir="data", chroma_path=chroma_dir)
    docs_after = db.get()
    # Number of docs should be the same
    assert len(docs) == len(docs_after), "Duplicate documents should not be added"
