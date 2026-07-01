import json
import os
import pytest
from src.mcp_utils import fetch_course_meta

def test_fetch_course_meta_from_file(monkeypatch):
    # Ensure environment variable points to a non-existent endpoint
    monkeypatch.setenv("MCP_ENDPOINT", "http://localhost:9999/nonexistent.json")
    # Use the local file
    result = fetch_course_meta("Instructor")
    assert "Instructor" in result
    assert "Dr. Jane Doe" in result

def test_fetch_course_meta_http(monkeypatch):
    # Mock httpx.get to return a fake JSON
    class DummyResponse:
        def __init__(self, json_data):
            self._json = json_data
        def raise_for_status(self):
            pass
        def json(self):
            return self._json
    def mock_get(url, timeout):
        return DummyResponse({"Mock Key": "Mock Value"})
    monkeypatch.setattr("httpx.get", mock_get)
    result = fetch_course_meta("Mock Key")
    assert "Mock Key" in result
    assert "Mock Value" in result
