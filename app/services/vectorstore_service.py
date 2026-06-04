from pathlib import Path
import shutil
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app.core.settings import settings
from app.core.embedding_factory import EmbeddingFactory
from app.core.logger import logger
from app.services.pdf_service import PDFService

class VectorStoreService:
    @staticmethod
    def reset():
        path = Path(settings.vectorstore_dir)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        logger.info("Reset vectorstore")

    @staticmethod
    def exists():
        return (Path(settings.vectorstore_dir) / "index.faiss").exists()

    @staticmethod
    def build(provider: str | None = None):
        pdf_files = PDFService.list_pdfs()
        if not pdf_files:
            raise FileNotFoundError("Chưa có PDF trong data/pdfs.")

        documents = []

        for pdf in pdf_files:
            loader = PyPDFLoader(str(pdf))
            pages = loader.load()
            for page in pages:
                page.metadata["source_file"] = pdf.name
                page.metadata["source_path"] = str(pdf)
            documents.extend(pages)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = splitter.split_documents(documents)

        embeddings = EmbeddingFactory.create(provider)
        db = FAISS.from_documents(chunks, embeddings)

        Path(settings.vectorstore_dir).mkdir(parents=True, exist_ok=True)
        db.save_local(settings.vectorstore_dir)

        logger.info("Vectorstore built: %s files, %s chunks", len(pdf_files), len(chunks))

        return {
            "pdf_count": len(pdf_files),
            "chunk_count": len(chunks),
            "files": [p.name for p in pdf_files],
        }

    @staticmethod
    def load(provider: str | None = None):
        if not VectorStoreService.exists():
            raise FileNotFoundError("Chưa có vector database. Hãy rebuild Knowledge Base trước.")

        return FAISS.load_local(
            settings.vectorstore_dir,
            EmbeddingFactory.create(provider),
            allow_dangerous_deserialization=True,
        )

    @staticmethod
    def search(query: str, k: int | None = None, provider: str | None = None):
        k = k or settings.top_k
        db = VectorStoreService.load(provider)
        docs = db.similarity_search(query, k=k)

        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page", "unknown")
            content = doc.page_content.strip()
            formatted.append(
                f"[Nguồn {i}] File: {source} | Trang: {page}\n{content}"
            )

        return "\n\n---\n\n".join(formatted)
