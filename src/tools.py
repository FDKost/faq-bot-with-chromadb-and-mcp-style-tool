import json
import os
from typing import List

import httpx
from langchain.tools import BaseTool

from .ingestion import search_course_docs

MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://localhost:8000")

class SearchCourseDocsTool(BaseTool):
    name = "search_course_docs"
    description = "Search course documents in ChromaDB."
    def _run(self, query: str) -> str:
        results = search_course_docs(query)
        return "\n".join(results)

class FetchCourseMetaTool(BaseTool):
    name = "fetch_course_meta"
    description = "Fetch course metadata from the MCP mock server."
    def _run(self, query: str) -> str:
        # Simple heuristic: look for a date in the query
        response = httpx.get(f"{MOCK_SERVER_URL}/metadata")
        response.raise_for_status()
        data = response.json()
        # Return the first matching entry
        for entry in data:
            if entry.get("title") and entry["title"].lower() in query.lower():
                return json.dumps(entry, indent=2)
        return "No matching metadata found."

search_course_docs_tool = SearchCourseDocsTool()
fetch_course_meta_tool = FetchCourseMetaTool()
