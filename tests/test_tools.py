import json
from unittest.mock import patch

from src.tools import search_course_docs_tool, fetch_course_meta_tool

def test_search_course_docs_tool_returns_string():
    with patch("src.ingestion.search_course_docs") as mock_search:
        mock_search.return_value = ["doc1", "doc2"]
        result = search_course_docs_tool.run("query")
        assert result == "doc1\ndoc2"

def test_fetch_course_meta_tool_returns_string():
    # Mock the HTTP response
    with patch("httpx.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"title": "Lecture 2", "description": "Advanced topics", "date": "2023-09-08"}
        ]
        result = fetch_course_meta_tool.run("Lecture 2")
        assert json.loads(result)["title"] == "Lecture 2"
