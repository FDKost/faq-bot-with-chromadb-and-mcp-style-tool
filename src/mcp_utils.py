import json
from pathlib import Path
from typing import List, Dict

from langchain.tools import tool

@tool
def fetch_course_meta(query: str) -> List[Dict]:
    """
    Fetch course metadata that matches the query.
    The metadata is read from data/course_meta.json.
    """
    data_file = Path(__file__).parent.parent / "data" / "course_meta.json"
    with open(data_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Simple keyword matching
    query_lower = query.lower()
    matches = [
        item
        for item in meta
        if query_lower in item["title"].lower()
        or query_lower in item["description"].lower()
    ]
    return matches
