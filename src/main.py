import argparse
from src.vector_store_utils import load_faq_docs, create_vector_store
from src.langchain_agent import create_agent

def main():
    parser = argparse.ArgumentParser(description="FAQ Bot CLI")
    parser.add_argument(
        "--preset",
        action="store_true",
        help="Run preset questions instead of interactive mode",
    )
    args = parser.parse_args()

    # Load documents and create vector store
    docs = load_faq_docs()
    collection = create_vector_store(docs)

    # Create the LangChain agent
    agent = create_agent(collection)

    if args.preset:
        preset_questions = [
            "What is the deadline for assignment 1?",
            "How is grading determined?",
            "When is the next lecture?",
        ]
        for q in preset_questions:
            print(f"Q: {q}")
            print(f"A: {agent.run(q)}\n")
    else:
        print("Enter your questions (type 'quit' to exit):")
        while True:
            try:
                q = input("> ")
                if q.lower() in ("quit", "exit"):
                    break
                print(agent.run(q))
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

if __name__ == "__main__":
    main()
