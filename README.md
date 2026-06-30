# FAQ Bot with ChromaDB and MCP‑style Tool

This project implements a simple FAQ bot that can answer questions about course materials
using a local ChromaDB vector store and about course metadata using a mock MCP‑style
HTTP service. The bot is built with LangChain and can be interacted with via a
command‑line interface.

## Project Structure

```
faq_bot/
├── src/
│   ├── cli.py          # CLI entry point
│   ├── agent.py        # Agent that routes queries
│   ├── ingestion.py    # Load markdown files into ChromaDB
│   ├── tools.py        # LangChain tools for searching and metadata
│   ├── mock_server.py  # FastAPI mock server for metadata
│   ├── main.py         # Entry point for the CLI
│   └── __init__.py
├── data/
│   ├── sample.md        # Example course material
│   └── course_meta.json # Example metadata
├── tests/
│   ├── test_ingestion.py
│   ├── test_tools.py
│   └── test_agent.py
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

* Python 3.10 or newer
* Ollama running locally with the `llama3` model and the `nomic-embed-text` model
  (see https://ollama.com/ for installation)

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/faq_bot.git
cd faq_bot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Running the Mock Server

The metadata tool queries a local FastAPI server. Start it with:

```bash
uvicorn src.mock_server:app --reload
```

The server will be available at `http://localhost:8000`.

## Loading the FAQ into ChromaDB

```bash
python -m src.cli init
```

This reads all `.md` files in `data/`, splits them into chunks, embeds them with
Ollama embeddings, and persists the vector store at `./chroma_faq`.

## Using the Bot

### Sample Questions

```bash
python -m src.cli sample
```

This runs three predefined questions:
1. “What is the deadline for assignment 1?” (Chroma)
2. “Explain the grading policy.” (Chroma)
3. “What is the next lecture date?” (MCP)

### Interactive Mode

```bash
python -m src.cli interactive
```

Type any question and press Enter. Type `exit` to quit.

### Single Question

```bash
python -m src.cli ask "Your question here"
```

## Testing

Run the test suite with:

```bash
pytest
```

Make sure the mock server is running before testing the metadata tool.

## License

MIT
