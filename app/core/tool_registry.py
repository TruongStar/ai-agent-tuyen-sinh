from app.tools.knowledge_base import search_knowledge_base, lookup_admission_score, admission_faq
from app.tools.major_recommender import recommend_major
from app.tools.calculator import calculator
from app.tools.web_search import web_search

class ToolRegistry:
    @staticmethod
    def all_tools():
        return [
            search_knowledge_base,
            lookup_admission_score,
            recommend_major,
            admission_faq,
            calculator,
            web_search,
        ]

    @staticmethod
    def tool_names():
        return [tool.name for tool in ToolRegistry.all_tools()]
