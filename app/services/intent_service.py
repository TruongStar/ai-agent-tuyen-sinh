from app.core.llm_factory import LLMFactory
from app.core.prompts import INTENT_PROMPT

class IntentService:
    def __init__(self, provider: str, model: str | None = None):
        self.llm = LLMFactory.create(provider=provider, model=model, temperature=0)

    def classify(self, question: str) -> str:
        prompt = f"""{INTENT_PROMPT}

Câu hỏi:
{question}

Chỉ trả về đúng một intent.
"""
        try:
            result = self.llm.invoke(prompt)
            return str(result.content).strip()
        except Exception:
            return "general_chat"
