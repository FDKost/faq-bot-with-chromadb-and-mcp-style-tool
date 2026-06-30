from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("data/course_meta.json")

@app.get("/meta")
def get_meta(query: str):
    """
    Return course metadata that matches the query.
    """
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = [
        item
        for item in data
        if query.lower() in item.get("title", "").lower()
        or query.lower() in item.get("description", "").lower()
    ]
    return {"results": results}
