# FAQ Bot: ChromaDB + MCP‑style Tool

This project demonstrates a simple FAQ bot that uses **ChromaDB** for vector search and a mock metadata service (MCP‑style) for structured data.  
The bot is built with **LangChain** and can be interacted with via a command‑line interface.

## Features

- **Vector Search** – Load Markdown FAQ files into a persistent ChromaDB store and query them.
- **Metadata Service** – Fetch course metadata from a static JSON file.
- **LangChain Agent** – Routes queries to the appropriate tool (Chroma or MCP) and tags the answer with the source.
- **CLI** – Run preset questions or interactively ask any question.

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/faq-bot.git
   cd faq-bot
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If you plan to use the OpenAI LLM, set your API key:*

   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

4. **Run the bot**

   ```bash
   python src/main.py
   ```

   - Use `--preset` to run the three preset questions.
   - Without arguments, you can type any question interactively.

## Project Structure

```
faq-bot/
├── data/
│   ├── faq1.md
│   ├── faq2.md
│   ├── faq3.md
│   └── course_meta.json
├── src/
│   ├── agent.py          # Simple test agent
│   ├── chroma_utils.py   # ChromaDB helpers
│   ├── mcp_utils.py      # Metadata helpers
│   ├── langchain_agent.py
│   └── main.py
├── tests/
│   └── test_agent.py
├── chroma_faq/           # Persisted ChromaDB store (created on first run)
├── requirements.txt
└── README.md
```

## Running Tests

The repository includes a simple test suite for the legacy `Agent` class.

```bash
pytest
```

## Extending the Bot

- **Add more FAQ files** – Drop additional `.md` files into the `data/` folder and rerun `python src/main.py` to rebuild the vector store.
- **Update metadata** – Edit `data/course_meta.json` with new entries.
- **Replace the LLM** – Swap `OpenAI` for another provider in `src/langchain_agent.py`.

## License

MIT License
