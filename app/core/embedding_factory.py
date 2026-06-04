from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.settings import settings

class EmbeddingFactory:
    @staticmethod
    def create(provider: str | None = None):
        provider = (provider or settings.model_provider).lower()

        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("Thiếu OPENAI_API_KEY để tạo embedding.")
            return OpenAIEmbeddings(
                model=settings.openai_embedding_model,
                api_key=settings.openai_api_key,
            )

        if provider == "gemini":
            if not settings.google_api_key:
                raise ValueError("Thiếu GOOGLE_API_KEY để tạo embedding.")
            return GoogleGenerativeAIEmbeddings(
                model=settings.gemini_embedding_model,
                google_api_key=settings.google_api_key,
            )

        raise ValueError("Provider embedding không hợp lệ.")
