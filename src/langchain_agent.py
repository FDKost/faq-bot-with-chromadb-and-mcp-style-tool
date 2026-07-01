import json
from langchain_ollama import Ollama
from langchain.agents import Tool, initialize_agent, AgentType
from src.vector_store_utils import search_course_docs
from src.mcp_utils import fetch_course_meta

def qdrant_search_tool(client) -> Tool:
    def _search(query: str) -> str:
        results = search_course_docs(client, query, k=3)
        if not results:
            return "No relevant documents found.\nSource: qdrant"
        return "\n\n".join(
            [f"Source {i+1}:\n{res['page_content']}" for i, res in enumerate(results)]
        ) + "\nSource: qdrant"
    return Tool(
        name="Qdrant Search",
        func=_search,
        description="Search the FAQ stored in Qdrant. Use this for general course questions."
    )

def mcp_meta_tool() -> Tool:
    def _meta(query: str) -> str:
        return fetch_course_meta(query) + "\nSource: mcp_meta"
    return Tool(
        name="MCP Metadata",
        func=_meta,
        description="Fetch metadata about the course from the MCP service."
    )

def create_agent(client):
    tools = [qdrant_search_tool(client), mcp_meta_tool()]
    llm = Ollama(model="llama3")
    system_prompt = (
        "You are a helpful assistant for a course. "
        "Use the 'Qdrant Search' tool for general FAQ questions. "
        "Use the 'MCP Metadata' tool for questions about course schedule, modules, or lessons. "
        "Always include a source tag in your answer: 'Source: qdrant' or 'Source: mcp_meta'."
    )
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=False,
        agent_kwargs={"system_message": system_prompt},
    )
    return agent
