import argparse

from src.langchain_agent import LangChainAgent
from src.chroma_utils import load_faq_to_chroma

def main():
    # Ensure the vector store is loaded
    print("Loading FAQ into ChromaDB...")
    load_faq_to_chroma()
    print("Vector store ready.\n")

    agent = LangChainAgent()

    parser = argparse.ArgumentParser(description="FAQ Bot CLI")
    parser.add_argument(
        "--preset",
        action="store_true",
        help="Run preset questions (two for Chroma, one for MCP).",
    )
    args = parser.parse_args()

    if args.preset:
        presets = [
            "Explain the grading policy.",
            "What is the deadline for assignment 1?",
            "What is the next lecture date?",
        ]
        for q in presets:
            print(f"Q: {q}")
            print(f"A: {agent.answer(q)}\n")
    else:
        print("Enter your question (type 'exit' to quit):")
        while True:
            q = input("> ")
            if q.lower() in ("exit", "quit"):
                break
            print(f"A: {agent.answer(q)}\n")

if __name__ == "__main__":
    main()
