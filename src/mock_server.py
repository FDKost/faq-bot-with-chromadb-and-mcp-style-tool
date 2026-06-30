from fastapi import FastAPI
import json
import os

app = FastAPI()

DATA_FILE = os.getenv("DATA_FILE", "data/course_meta.json")

@app.get("/metadata")
def get_metadata():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
