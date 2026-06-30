import json
from fastapi.testclient import TestClient
import pytest

from src.mock_server import app as mock_app
from src.tools import search_course_docs_tool, fetch_course_meta_tool

@pytest.fixture
def mock_server():
    client = TestClient(mock_app)
    return client

def test_search_course_docs_tool():
    # Ensure ChromaDB is populated
    from src.ingestion import load_faq_to_chroma
    load_faq_to_chroma(data_dir="data", chroma_path="chroma_faq_test")
    # Call tool
    result = search_course_docs_tool("assignment")
    assert "source: chroma" in result
    assert len(result) > 0

def test_fetch_course_meta_tool(mock_server):
    # Mock server already running via TestClient
    result = fetch_course_meta_tool("Lecture 2")
    assert "source: mcp_meta" in result
    assert "Lecture 2" in result
