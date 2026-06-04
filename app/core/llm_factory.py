from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.settings import settings

class LLMFactory:
    @staticmethod
    def create(provider: str | None = None, model: str | None = None, temperature: float | None = None):
        provider = (provider or settings.model_provider).lower()
        temperature = settings.temperature if temperature is None else temperature

        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("Thiếu OPENAI_API_KEY trong file .env")
            return ChatOpenAI(
                model=model or settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=temperature,
                streaming=True,
            )

        if provider == "gemini":
            if not settings.google_api_key:
                raise ValueError("Thiếu GOOGLE_API_KEY trong file .env")
            return ChatGoogleGenerativeAI(
                model=model or settings.gemini_model,
                google_api_key=settings.google_api_key,
                temperature=temperature,
            )

        raise ValueError("Provider không hợp lệ. Chỉ nhận openai hoặc gemini.")
