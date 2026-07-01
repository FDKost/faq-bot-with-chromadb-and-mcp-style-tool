import os
import json
import httpx

def fetch_course_meta(query: str) -> str:
    """
    Fetch metadata about the course from the MCP service.
    Tries to GET from MCP_ENDPOINT; falls back to local JSON file.
    """
    endpoint = os.getenv("MCP_ENDPOINT")
    if endpoint:
        try:
            resp = httpx.get(endpoint, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
            return f"{query}: {data.get(query, 'Not found')}"
        except Exception:
            pass
    # Fallback to local file
    local_path = os.path.join("data", "course_meta.json")
    with open(local_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return f"{query}: {data.get(query, 'Not found')}"
