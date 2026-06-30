import typer
from .agent import build_agent
from .ingestion import load_faq_to_chroma

app = typer.Typer()

SAMPLE_QUESTIONS = [
    ("What is the deadline for assignment 1?", "chroma"),
    ("Explain the grading policy.", "chroma"),
    ("What is the next lecture date?", "mcp_meta")
]

@app.command()
def init():
    """Load FAQ into ChromaDB."""
    load_faq_to_chroma()
    typer.echo("FAQ loaded into ChromaDB.")

@app.command()
def sample():
    """Run sample questions."""
    agent = build_agent()
    for q, _ in SAMPLE_QUESTIONS:
        typer.echo(f"Q: {q}")
        answer = agent.run(q)
        typer.echo(f"A: {answer}\n")

@app.command()
def ask(question: str):
    """Ask a question."""
    agent = build_agent()
    answer = agent.run(question)
    typer.echo(f"Answer: {answer}")

@app.command()
def interactive():
    """Interactive mode."""
    agent = build_agent()
    typer.echo("Enter your question (type 'exit' to quit):")
    while True:
        q = input("> ")
        if q.lower() in ("exit", "quit"):
            break
        answer = agent.run(q)
        typer.echo(f"Answer: {answer}")

if __name__ == "__main__":
    app()
