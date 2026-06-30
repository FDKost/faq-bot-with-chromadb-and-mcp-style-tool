import json
from pathlib import Path
from typing import List, Dict

def fetch_course_meta(query: str) -> List[Dict]:
    """
    Fetch course metadata from a static JSON file.
    Returns a list of matching entries where the query matches
    the title or description (case-insensitive).
    """
    data_file = Path(__file__).parent.parent / "data" / "course_meta.json"
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    query_lower = query.lower()
    results = [
        entry
        for entry in data
        if query_lower in entry["title"].lower()
        or query_lower in entry["description"].lower()
    ]
    return results
