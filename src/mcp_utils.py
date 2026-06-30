import json
from pathlib import Path
from typing import List, Dict

def fetch_course_meta(query: str) -> List[Dict]:
    """
    Fetch course metadata from a static JSON file.
    Returns a list of matching metadata entries.
    """
    meta_file = Path(__file__).parent.parent / "data" / "course_meta.json"
    with open(meta_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    query_lower = query.lower()
    matches = [
        item
        for item in data
        if query_lower in item.get("title", "").lower()
        or query_lower in item.get("description", "").lower()
    ]
    return matches
