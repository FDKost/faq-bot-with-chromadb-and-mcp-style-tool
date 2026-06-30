import json
from langchain_ollama import Ollama
from langchain.agents import Tool, initialize_agent, AgentType
from src.vector_store_utils import search_course_docs
from src.mcp_utils import fetch_course_meta

def chroma_search_tool(vector_store) -> Tool:
    def _search(query: str) -> str:
        results = search_course_docs(vector_store, query, k=3)
        if not results:
            return "No relevant documents found."
        return "\n\n".join(
            [f"Source {i+1}:\n{res['page_content']}" for i, res in enumerate(results)]
        ) + "\nSource: chroma"
    return Tool(
        name="Chroma Search",
        func=_search,
        description="Search the FAQ stored in Chroma. Use this for general course questions."
    )

def mcp_meta_tool() -> Tool:
    def _meta(query: str) -> str:
        return fetch_course_meta(query)
    return Tool(
        name="MCP Metadata",
        func=_meta,
        description="Fetch metadata about the course from the MCP service."
    )

def create_agent(vector_store):
    tools = [chroma_search_tool(vector_store), mcp_meta_tool()]
    llm = Ollama(model="llama3")
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
    )
    return agent
