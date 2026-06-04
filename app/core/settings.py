from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    model_provider: str = os.getenv("MODEL_PROVIDER", "openai").lower()

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    gemini_embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")

    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
    top_k: int = int(os.getenv("TOP_K", "6"))
    max_tool_result_chars: int = int(os.getenv("MAX_TOOL_RESULT_CHARS", "6000"))

    pdf_dir: str = "data/pdfs"
    vectorstore_dir: str = "data/vectorstore"
    chat_history_dir: str = "data/chat_history"
    export_dir: str = "data/exports"
    log_dir: str = "logs"

settings = Settings()
