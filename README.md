# FAQ Bot: ChromaDB + MCP‑style Tool

This project demonstrates a simple FAQ bot that uses **ChromaDB** for vector search and a mock metadata service (MCP‑style) for structured data.  
The bot is built with **LangChain** and can be interacted with via a command‑line interface.

## Features

- **Vector Search** – Load Markdown FAQ files into a persistent ChromaDB store and query them using the `nomic-embed-text` model from Ollama.
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

4. **Pull the Ollama models**

   The bot uses two Ollama models:

   - `nomic-embed-text` – for embeddings
   - `llama3` – for the LLM

   Install them with:

   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3
   ```

5. **Run the bot**

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
│   ├── vector_store_utils.py   # ChromaDB helpers
│   ├── mcp_utils.py            # Metadata helpers
│   ├── langchain_agent.py
│   ├── main.py
│   └── agent.py                # Legacy simple agent (unused)
├── chroma_faq/                 # Persisted ChromaDB store (created on first run)
├── requirements.txt
└── README.md
```

## Extending the Bot

- **Add more FAQ files** – Drop additional `.md` files into the `data/` folder and rerun `python src/main.py` to rebuild the vector store.
- **Update metadata** – Edit `data/course_meta.json` with new entries.
- **Replace the LLM** – Swap `Ollama` for another provider in `src/langchain_agent.py`.

## License

MIT License
