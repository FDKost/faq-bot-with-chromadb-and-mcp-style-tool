# FAQ Bot with ChromaDB and MCP-style Tool

This project implements a simple FAQ bot that can answer questions about course materials
using a local ChromaDB vector store and about course metadata using a mock MCP-style
HTTP service. The bot is built with LangChain and can be interacted with via a
command‑line interface.

## Project Structure

```
faq_bot/
├── src/
│   ├── main.py          # CLI entry point
│   ├── ingestion.py     # Load markdown files into ChromaDB
│   ├── tools.py         # LangChain tools for searching and metadata
│   ├── agent.py         # Agent that routes queries
│   └── mock_server.py   # FastAPI mock server for metadata
├── data/
│   ├── sample.md        # Example course material
│   └── course_meta.json # Example metadata
├── tests/
│   ├── test_ingestion.py
│   └── test_tools.py
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

* Python 3.10 or newer
* An OpenAI API key (for embeddings and LLM). Set it in a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

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
python -m src.main init
```

This reads all `.md` files in `data/`, splits them into chunks, embeds them with
OpenAI embeddings, and persists the vector store at `./chroma_faq`.

## Using the Bot

### Sample Questions

```bash
python -m src.main sample
```

This runs three predefined questions:
1. “What is the deadline for assignment 1?” (Chroma)
2. “Explain the grading policy.” (Chroma)
3. “What is the next lecture date?” (MCP)

### Interactive Mode

```bash
python -m src.main interactive
```

Type any question and press Enter. Type `exit` to quit.

### Single Question

```bash
python -m src.main ask "Your question here"
```

## Testing

Run the test suite with:

```bash
pytest
```

Make sure the mock server is running before testing the metadata tool.

## License

MIT
