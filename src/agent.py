# Legacy simple agent (unused in the current implementation)
from typing import Any

class Agent:
    """
    A very simple Agent that can route queries to either a Qdrant
    vector store or a mock metadata service.
    """

    def __init__(self, qdrant_client: Any, metadata_client: Any):
        self.qdrant_client = qdrant_client
        self.metadata_client = metadata_client

    def answer(self, question: str) -> str:
        """
        Return a canned answer based on the question content.
        """
        if "deadline" in question.lower():
            return "The deadline for assignment 1 is next Friday."
        if "grading policy" in question.lower():
            return "Grades are based on assignments, quizzes, and participation."
        if "lecture date" in question.lower():
            return self.metadata_client.get_next_lecture_date()
        return "I don't know the answer to that question."
