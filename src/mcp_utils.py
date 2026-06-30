import json
from pathlib import Path

def get_next_lecture_date() -> str:
    """
    Return a mock next lecture date.
    """
    return "Next lecture is on Monday, 10 AM."

def fetch_course_meta(query: str) -> str:
    """
    Fetch metadata about the course from a static JSON file.
    """
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
