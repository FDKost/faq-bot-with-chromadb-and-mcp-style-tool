import argparse
from src.vector_store_utils import load_faq_docs, create_vector_store
from src.langchain_agent import create_agent

def main():
    parser = argparse.ArgumentParser(description="FAQ Bot CLI")
    parser.add_argument(
        "--preset",
        type=str,
        default="",
        help="Comma-separated list of preset questions to run. If omitted, interactive mode is used.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive REPL mode.",
    )
    args = parser.parse_args()

    # Load documents and create vector store
    docs = load_faq_docs()
    collection = create_vector_store(docs)

    # Create the LangChain agent
    agent = create_agent(collection)

    if args.preset:
        preset_questions = [q.strip() for q in args.preset.split(",") if q.strip()]
        for q in preset_questions:
            print(f"Q: {q}")
            print(f"A: {agent.run(q)}\n")
    elif args.interactive:
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
    else:
        # Default to interactive if no flags provided
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
