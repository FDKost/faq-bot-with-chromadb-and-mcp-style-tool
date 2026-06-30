import argparse
import os
from pathlib import Path

from src.vector_store_utils import load_data_to_qdrant
from src.langchain_agent import LangChainAgent

def main():
    parser = argparse.ArgumentParser(description="FAQ Bot")
    parser.add_argument("--preset", action="store_true", help="Run preset questions")
    args = parser.parse_args()

    # Environment variables
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)
    collection_name = "faq_collection"

    data_dir = Path(__file__).parent.parent / "data"

    # Load data into Qdrant
    vector_store = load_data_to_qdrant(
        data_dir=str(data_dir),
        collection_name=collection_name,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key,
    )

    agent = LangChainAgent(vector_store)

    if args.preset:
        questions = [
            "What is the grading policy?",
            "When is the next lecture?",
            "What is the deadline for assignment 1?",
        ]
        for q in questions:
            print(f"\nQ: {q}")
            print(f"A: {agent.answer(q)}")
    else:
        print("Enter your question (type 'exit' to quit):")
        while True:
            q = input("> ")
            if q.lower() in ("exit", "quit"):
                break
            print(f"A: {agent.answer(q)}")

if __name__ == "__main__":
    main()
