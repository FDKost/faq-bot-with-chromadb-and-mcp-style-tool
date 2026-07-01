import pytest
from src.langchain_agent import create_agent
from src.vector_store_utils import create_vector_store, load_faq_docs

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
        return []

def test_agent_routes_to_mcp(monkeypatch):
    # Mock fetch_course_meta to return a predictable string
    monkeypatch.setattr("src.mcp_utils.fetch_course_meta", lambda q: f"MockMeta: {q}")
    client = DummyClient()
    agent = create_agent(client)
    response = agent.run("When is the next lecture?")
    assert "Source: mcp_meta" in response
    assert "MockMeta" in response

def test_agent_routes_to_qdrant(monkeypatch):
    # Create a simple doc with known content
    docs = [{"page_content": "This is a content question about course", "metadata": {"source": "test.md"}}]
    client = DummyClient()
    # Monkeypatch search to return a dummy result
    def mock_search(collection_name, query_vector, limit):
        return [type("Point", (object,), {"payload": {"source": "test.md"}, "score": 1.0})()]
    client.search = mock_search
    agent = create_agent(client)
    response = agent.run("How many students?")
    assert "Source: qdrant" in response
