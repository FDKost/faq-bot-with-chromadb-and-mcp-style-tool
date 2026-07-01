import os
import json
import pytest
from src.vector_store_utils import load_faq_docs, create_vector_store, search_course_docs

class DummyPoint:
    def __init__(self, payload, score=1.0):
        self.payload = payload
        self.score = score

class DummyClient:
    def __init__(self):
        self.collections = set()
        self.points = []

    def get_collections(self):
        return type("obj", (object,), {"collections": self.collections})()

    def create_collection(self, collection_name, vectors_config):
        self.collections.add(collection_name)

    def upsert(self, collection_name, points):
        self.points.extend(points)

    def search(self, collection_name, query_vector, limit):
        # Return dummy results based on query_vector content
        return [DummyPoint({"source": f"doc_{i}"}, score=1.0) for i in range(limit)]

@pytest.fixture
def dummy_client(monkeypatch):
    monkeypatch.setattr("src.vector_store_utils.QdrantClient", lambda *args, **kwargs: DummyClient())
    return DummyClient()

def test_load_faq_docs(tmp_path, monkeypatch):
    # Create a dummy markdown file
    md_path = tmp_path / "test.md"
    md_path.write_text("Hello world\n\nMore content.")
    monkeypatch.chdir(tmp_path)
    docs = load_faq_docs()
    assert len(docs) > 0
    assert any("Hello world" in d["page_content"] for d in docs)

def test_create_vector_store(dummy_client):
    docs = [{"page_content": "Test content", "metadata": {"source": "test.md"}}]
    client = create_vector_store(docs)
    assert isinstance(client, DummyClient)
    assert len(client.points) == len(docs)

def test_search_course_docs(dummy_client):
    client = DummyClient()
    results = search_course_docs(client, "Grading", k=2)
    assert len(results) == 2
    assert all("doc_" in r["page_content"] for r in results)
