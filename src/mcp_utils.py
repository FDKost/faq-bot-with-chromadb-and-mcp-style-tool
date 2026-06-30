import json
from pathlib import Path
from typing import List, Dict

def fetch_course_meta(query: str) -> List[Dict]:
    """
    Load the course metadata JSON and return entries that match the query
    in either the title or description (case‑insensitive).
    """
    data_path = Path(__file__).parent.parent / "data" / "course_meta.json"
    with open(data_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    query_lower = query.lower()
    results = [
        item
        for item in meta
        if query_lower in item.get("title", "").lower()
        or query_lower in item.get("description", "").lower()
    ]
    return results
