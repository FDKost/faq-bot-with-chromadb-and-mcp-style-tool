import json
import os
from pathlib import Path
import httpx

def get_next_lecture_date() -> str:
    """
    Return a mock next lecture date.
    """
    return "Next lecture is on Monday, 10 AM."

def fetch_course_meta(query: str) -> str:
    """
    Fetch metadata about the course from a local HTTP endpoint or a static JSON file.
    The function first attempts to GET from a predefined URL. If the request fails,
    it falls back to reading a local file.
    """
    # Try HTTP GET first
    endpoint = os.getenv("MCP_ENDPOINT", "http://localhost:8000/course_meta.json")
    try:
        response = httpx.get(endpoint, timeout=2.0)
        response.raise_for_status()
        data = response.json()
    except Exception:
        # Fallback to local file
        meta_path = Path("data/course_meta.json")
        if not meta_path.exists():
            return "Metadata file not found."
        with meta_path.open() as f:
            data = json.load(f)

    # Simple keyword search
    for key, value in data.items():
        if key.lower() in query.lower():
            return f"{key}: {value}"
    return "No metadata found for query."
