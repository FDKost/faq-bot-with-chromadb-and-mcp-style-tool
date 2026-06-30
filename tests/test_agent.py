import unittest
from src.langchain_agent import LangChainAgent
from src.chroma_utils import load_faq_to_chroma

class TestLangChainAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_faq_to_chroma()
        cls.agent = LangChainAgent()

    def test_grading_policy(self):
        ans = self.agent.answer("What is the grading policy?")
        self.assertIn("grading policy", ans.lower())

    def test_lecture_date(self):
        ans = self.agent.answer("When is the next lecture?")
        self.assertIn("lecture", ans.lower())

if __name__ == "__main__":
    unittest.main()
