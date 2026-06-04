# app/api/api_server.py
# API service cho AI Agent tuyển sinh ICTU
# Chạy: uvicorn app.api.api_server:app --reload --host 0.0.0.0 --port 8000

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PDF_DIR = Path("data/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="ICTU AI Agent Admissions API",
    description="API hỏi đáp tuyển sinh ICTU, quản lý PDF Knowledge Base và biểu mẫu",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    user_type: Optional[str] = "student"


class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []


def get_agent_answer(question: str) -> ChatResponse:
    """
    Chỗ này kết nối với Agent thật của bạn.
    Ví dụ thay bằng:
        from app.core.agent import agent
        result = agent.run(question)
    """
    answer = "API đã nhận câu hỏi. Hãy kết nối hàm get_agent_answer() với Agent/RAG hiện tại của bạn."
    return ChatResponse(answer=answer, sources=[])


@app.get("/")
def root():
    return {
        "status": "ok",
        "name": "ICTU AI Agent Admissions API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    return get_agent_answer(request.question)


@app.get("/pdfs")
def list_pdfs():
    files = sorted(PDF_DIR.glob("*.pdf"))
    return {
        "count": len(files),
        "files": [file.name for file in files],
    }


@app.post("/pdfs/upload")
async def upload_pdf(files: List[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File không phải PDF: {file.filename}")
        save_path = PDF_DIR / file.filename
        content = await file.read()
        save_path.write_bytes(content)
        saved_files.append(file.filename)
    return {"message": "Upload thành công", "files": saved_files}


@app.delete("/pdfs/{filename}")
def delete_pdf(filename: str):
    file_path = PDF_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Không tìm thấy file")
    file_path.unlink()
    return {"message": f"Đã xóa {filename}"}


@app.post("/kb/rebuild")
def rebuild_kb():
    """
    Kết nối với service rebuild KB thật của bạn.
    Ví dụ:
        from app.services.knowledge_base import rebuild_vectorstore
        result = rebuild_vectorstore()
    """
    return {"message": "Endpoint rebuild đã sẵn sàng. Hãy nối với service rebuild vectorstore hiện tại."}
