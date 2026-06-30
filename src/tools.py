import requests
from typing import List

from langchain.tools import tool

from ingestion import search_course_docs

@tool
def search_course_docs_tool(query: str) -> str:
    """
    Search course documents in ChromaDB and return relevant snippets.
    """
    snippets: List[str] = search_course_docs(query)
    if not snippets:
        return "No relevant documents found.\nsource: chroma"
    return "\n".join(snippets) + "\nsource: chroma"

def fetch_course_meta(query: str) -> dict:
    """
    Perform an HTTP GET request to the local mock server to retrieve course metadata.
    """
    url = "http://localhost:8000/meta"
    params = {"query": query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@tool
def fetch_course_meta_tool(query: str) -> str:
    """
    Fetch course metadata from the mock server and return it as a string.
    """
    meta = fetch_course_meta(query)
    return f"{meta}\nsource: mcp_meta"
