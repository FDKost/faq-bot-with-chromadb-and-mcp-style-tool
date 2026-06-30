from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage

from .tools import search_course_docs_tool, fetch_course_meta_tool

def build_agent():
    """
    Build a LangChain agent that can route queries to either the Chroma search tool
    or the MCP metadata tool based on the content of the query.
    """
    tools = [search_course_docs_tool, fetch_course_meta_tool]
    llm = ChatOpenAI(temperature=0)

    system_prompt = SystemMessage(
        content=(
            "You are a helpful FAQ bot. "
            "Use the search_course_docs tool for questions about course materials. "
            "Use the fetch_course_meta tool for questions about schedule or metadata. "
            "Return the answer and include a source annotation: source: chroma or source: mcp_meta."
        )
    )

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        agent_kwargs={"prefix_messages": [system_prompt]},
    )
    return agent
