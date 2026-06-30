import os
import pytest
from src.agent import build_agent

def test_agent_routing():
    agent = build_agent()
    # Question about assignment -> should use chroma
    answer_chroma = agent.run("What is the deadline for assignment 1?")
    assert "source: chroma" in answer_chroma

    # Question about schedule -> should use mcp_meta
    answer_meta = agent.run("When is the next lecture?")
    assert "source: mcp_meta" in answer_meta
