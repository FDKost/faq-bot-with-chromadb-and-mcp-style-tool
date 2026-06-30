import json
from typing import List

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI

from src.chroma_utils import search_course_docs
from src.mcp_utils import fetch_course_meta

def chroma_search_tool() -> Tool:
    """
    Tool that searches the Chroma vector store.
    """
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
        description="Search the FAQ stored in ChromaDB. Use this for general course questions.",
    )

def mcp_meta_tool() -> Tool:
    """
    Tool that fetches course metadata.
    """
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
        description="Fetch course metadata. Use this for questions about deadlines, lecture dates, etc.",
    )

class LangChainAgent:
    """
    A LangChain agent that routes queries to either the Chroma search tool
    or the MCP metadata tool based on the question content.
    """
    def __init__(self, llm=None):
        self.llm = llm or OpenAI(temperature=0)
        self.tools = [chroma_search_tool(), mcp_meta_tool()]
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
        )

    def answer(self, question: str) -> str:
        """
        Run the agent on the question and append a source tag.
        """
        response = self.agent.run(question)

        # Determine source based on content markers
        if "Source" in response:
            source = "chroma"
        elif "Meta" in response:
            source = "mcp_meta"
        else:
            source = "unknown"

        return f"{response}\nSource: {source}"
