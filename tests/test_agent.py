import pytest
from src.agent import Agent

class DummyMetadataClient:
    def get_next_lecture_date(self):
        return "2024-07-15"

class DummyQdrantClient:
    pass

def test_agent_answer_qdrant():
    agent = Agent(DummyQdrantClient(), DummyMetadataClient())
    assert agent.answer("What is the deadline for assignment 1?") == "The deadline for assignment 1 is next Friday."

def test_agent_answer_grading():
    agent = Agent(DummyQdrantClient(), DummyMetadataClient())
    assert agent.answer("Explain the grading policy.") == "Grades are based on assignments, quizzes, and participation."

def test_agent_answer_metadata():
    agent = Agent(DummyQdrantClient(), DummyMetadataClient())
    assert agent.answer("What is the next lecture date?") == "2024-07-15"

def test_agent_unknown():
    agent = Agent(DummyQdrantClient(), DummyMetadataClient())
    assert agent.answer("Random question") == "I don't know the answer to that question."
