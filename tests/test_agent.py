import os
from unittest.mock import patch

from src.agent import build_agent

def test_agent_builds_and_runs(tmp_path):
    # Patch the tools to return deterministic outputs
    with patch("src.tools.search_course_docs_tool") as mock_search_tool:
        mock_search_tool.run.return_value = "Chroma answer snippet"
        with patch("src.tools.fetch_course_meta_tool") as mock_meta_tool:
            mock_meta_tool.run.return_value = "Meta answer snippet"
            # Patch the LLM to avoid real Ollama calls
            with patch("src.agent.Ollama") as MockLLM:
                MockLLM.return_value = MockLLM
                agent = build_agent()
                # Run a query that should trigger the search tool
                answer = agent.run("What is the deadline for assignment 1?")
                assert "Chroma answer snippet" in answer
                # Run a query that should trigger the meta tool
                answer_meta = agent.run("What is the next lecture date?")
                assert "Meta answer snippet" in answer_meta
