import json
from tools import search_course_docs_tool, fetch_course_meta_tool

def test_search_course_docs_tool():
    result = search_course_docs_tool("assignment")
    assert "source: chroma" in result

def test_fetch_course_meta_tool():
    # The mock server must be running on localhost:8000 before running this test
    result = fetch_course_meta_tool("schedule")
    assert "source: mcp_meta" in result
