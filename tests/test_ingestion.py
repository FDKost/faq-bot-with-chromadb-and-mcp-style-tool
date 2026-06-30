import os
import shutil
import tempfile
from unittest.mock import patch

import pytest

from src.ingestion import load_faq_to_chroma, CHROMA_DB_PATH

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d

def test_load_faq_to_chroma_creates_db(tmp_path):
    # Ensure the ChromaDB directory is clean
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)

    # Patch embeddings to avoid real Ollama calls
    with patch("src.ingestion.OllamaEmbeddings") as MockEmbeddings:
        MockEmbeddings.return_value = MockEmbeddings
        load_faq_to_chroma(data_dir="data", chroma_path=str(tmp_path))
        # Check that the ChromaDB directory was created
        assert os.path.isdir(os.path.join(tmp_path, "chroma_faq"))

def test_load_faq_no_md_files(tmp_path):
    # Create an empty temp directory
    empty_dir = os.path.join(tmp_path, "empty")
    os.makedirs(empty_dir, exist_ok=True)
    with pytest.raises(ValueError):
        load_faq_to_chroma(data_dir=empty_dir, chroma_path=str(tmp_path))
