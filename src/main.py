import argparse
import os
from pathlib import Path

from src.vector_store_utils import load_data_to_chroma
from src.langchain_agent import LangChainAgent

def main():
    parser = argparse.ArgumentParser(description="FAQ Bot")
    parser.add_argument("--preset", action="store_true", help="Run preset questions")
    args = parser.parse_args()

    data_dir = Path(__file__).parent.parent / "data"

    # Load data into Chroma
    collection = load_data_to_chroma(
        data_dir=str(data_dir),
        collection_name="faq_collection",
        persist_dir="./chroma_faq",
    )

    agent = LangChainAgent(collection)

    if args.preset:
        questions = [
            "What is the grading policy?",
            "What is the lecture schedule?",
            "When is the next lecture?",
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
