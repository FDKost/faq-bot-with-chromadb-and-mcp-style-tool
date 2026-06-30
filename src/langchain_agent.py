import json
from langchain_ollama import Ollama
from langchain.agents import Tool, initialize_agent, AgentType
from src.chroma_utils import search_course_docs
from src.mcp_utils import fetch_course_meta

def chroma_search_tool() -> Tool:
    def _search(query: str) -> str:
        results = search_course_docs(query)
        if not results:
            return "No relevant documents found."
        return "\n\n".join(
            [f"Source {i+1}:\n{res['content']}" for i, res in enumerate(results)]
        )
    return Tool(
        name="Chroma Search",
        func=_search,
        description="Search the FAQ stored in ChromaDB. Use this for general course questions."
    )

def mcp_meta_tool() -> Tool:
    def _meta(query: str) -> str:
        results = fetch_course_meta(query)
        if not results:
            return "No matching metadata found."
        return "\n\n".join(
            [f"Meta {i+1}:\n{json.dumps(res, indent=2)}" for i, res in enumerate(results)]
        )
    return Tool(
        name="MCP Meta",
        func=_meta,
        description="Fetch course metadata. Use this for questions about deadlines, lecture dates, etc."
    )

class LangChainAgent:
    def __init__(self, llm=None):
        self.llm = llm or Ollama(model="llama3", temperature=0)
        self.tools = [chroma_search_tool(), mcp_meta_tool()]
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            agent_kwargs={
                "system_message": (
                    "You are a helpful assistant. Use the Chroma Search tool for general FAQ questions "
                    "and the MCP Meta tool for metadata queries. After providing the answer, "
                    "include a source tag: 'Source: chroma' or 'Source: mcp_meta'."
                )
            },
        )

    def answer(self, question: str) -> str:
        response = self.agent.run(question)
        # Determine source based on content markers
        if "Source" in response:
            source = "chroma"
        elif "Meta" in response:
            source = "mcp_meta"
        else:
            source = "unknown"
        return f"{response}\nSource: {source}"
