import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).parent.parent / "data"

def fetch_course_meta(query: str) -> List[Dict]:
    """
    Fetch course metadata entries that match the query string.
    """
    meta_path = DATA_DIR / "course_meta.json"
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    query_lower = query.lower()
    results = []
    for entry in data:
        if query_lower in entry.get("title", "").lower() or query_lower in entry.get("description", "").lower():
            results.append(entry)
    return results
