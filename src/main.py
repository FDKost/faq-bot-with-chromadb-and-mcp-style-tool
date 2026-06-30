import argparse
from src.langchain_agent import LangChainAgent
from src.chroma_utils import load_faq_to_chroma

PRESET_QUESTIONS = [
    ("What is the grading policy?", "chroma"),
    ("When is the next lecture?", "mcp_meta"),
    ("How are assignments graded?", "chroma"),
]

def main():
    parser = argparse.ArgumentParser(description="FAQ Bot CLI")
    parser.add_argument("--preset", action="store_true", help="Run preset questions")
    args = parser.parse_args()

    # Ensure Chroma store is loaded
    load_faq_to_chroma()

    agent = LangChainAgent()

    if args.preset:
        for q, _ in PRESET_QUESTIONS:
            print(f"\nQ: {q}")
            ans = agent.answer(q)
            print(f"A: {ans}")
    else:
        print("Enter your question (type 'exit' to quit):")
        while True:
            q = input("> ")
            if q.lower() in ("exit", "quit"):
                break
            ans = agent.answer(q)
            print(f"A: {ans}")

if __name__ == "__main__":
    main()
