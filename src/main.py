import argparse
import sys
from src.vector_store_utils import load_faq_docs, create_vector_store
from src.langchain_agent import create_agent

def run_preset_questions(preset: str, agent):
    questions = [q.strip() for q in preset.split(",") if q.strip()]
    for q in questions:
        print(f"\nQuestion: {q}")
        answer = agent.run(q)
        print(f"Answer:\n{answer}")

def interactive_mode(agent):
    print("Enter your question (type 'exit' to quit):")
    while True:
        q = input("> ")
        if q.lower() in ("exit", "quit"):
            break
        answer = agent.run(q)
        print(f"Answer:\n{answer}")

def main():
    parser = argparse.ArgumentParser(description="FAQ Bot CLI")
    parser.add_argument("--preset", type=str, help="Comma‑separated preset questions")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    args = parser.parse_args()

    # Load vector store
    docs = load_faq_docs()
    client = create_vector_store(docs)
    agent = create_agent(client)

    if args.preset:
        run_preset_questions(args.preset, agent)
    elif args.interactive:
        interactive_mode(agent)
    else:
        print("No mode selected. Use --preset or --interactive.")
        sys.exit(1)

if __name__ == "__main__":
    main()
