import json
from langchain_ollama import Ollama
from langchain.agents import Tool, initialize_agent, AgentType
from src.vector_store_utils import search_course_docs
from src.mcp_utils import fetch_course_meta

def qdrant_search_tool(vector_store) -> Tool:
    def _search(query: str) -> str:
        results = search_course_docs(vector_store, query, k=3)
        if not results:
            return "No relevant documents found."
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
        results = fetch_course_meta(query)
        if not results:
            return "No matching metadata found."
        return "\n\n".join(
            [f"Meta {i+1}:\n{json.dumps(res, indent=2)}" for i, res in enumerate(results)]
        ) + "\nSource: mcp_meta"
    return Tool(
        name="MCP Meta",
        func=_meta,
        description="Fetch course metadata. Use this for questions about deadlines, lecture dates, etc."
    )

class LangChainAgent:
    def __init__(self, vector_store, llm=None):
        self.llm = llm or Ollama(model="llama3", temperature=0)
        self.tools = [qdrant_search_tool(vector_store), mcp_meta_tool()]
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            agent_kwargs={
                "system_message": (
                    "You are a helpful assistant. Use the Qdrant Search tool for general FAQ questions "
                    "and the MCP Meta tool for metadata queries. After providing the answer, "
                    "include a source tag: 'Source: qdrant' or 'Source: mcp_meta'."
                )
            },
        )

    def answer(self, question: str) -> str:
        response = self.agent.run(question)
        return response
