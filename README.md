# FAQ‑бот: ChromaDB + MCP‑style tool

## Requirements
- [high] Use ChromaDB for local FAQ storage: Create a data/ folder with 2–3 .md files. Implement load_faq_to_chroma() that chunks the markdown, embeds with Ollama nomic‑embed‑text, and persists the vector store in ./chroma_faq. Provide a search_course_docs(query, k=3) tool that queries this store.
- [high] Implement MCP‑style metadata tool: Create fetch_course_meta(query) that performs an HTTP GET to a local mock server (e.g., python -m http.server) or reads a static JSON file. Wrap it as a LangChain tool (using @tool or httpx). Ensure it is the only external tool used.
- [high] Build routing agent: Configure a LangChain agent (or LangGraph) with a system prompt that instructs the model to use search_course_docs for content questions and fetch_course_meta for schedule/metadata questions. The agent’s response must include a source tag: "source: chroma" or "source: mcp_meta".
- [normal] Provide CLI interface: Implement a command‑line interface that runs three preset questions (two targeting Chroma, one targeting MCP) and supports an interactive mode for arbitrary queries. The CLI should display the agent’s answer and the source tag.
- [normal] Documentation and packaging: Add a README that explains the setup (install dependencies, run mock server, start the bot). Ensure the project runs with python 3.10+, pip install requirements, and can be executed via a single script.
