from langchain_core.tools import tool
from app.services.vectorstore_service import VectorStoreService
from app.core.settings import settings

@tool
def search_knowledge_base(query: str) -> str:
    """Tra cứu PDF Knowledge Base về ngành học, học phí, chỉ tiêu, tổ hợp xét tuyển, chương trình đào tạo."""
    try:
        result = VectorStoreService.search(query=query, k=settings.top_k)
        if not result.strip():
            return "Không tìm thấy thông tin liên quan trong Knowledge Base."
        return result[:settings.max_tool_result_chars]
    except Exception as exc:
        return f"Lỗi Knowledge Base: {exc}"

@tool
def lookup_admission_score(query: str) -> str:
    """Tra cứu điểm chuẩn, điểm trúng tuyển, mã ngành, phương thức xét tuyển theo dữ liệu PDF."""
    try:
        q = f"điểm chuẩn điểm trúng tuyển mã ngành phương thức xét tuyển {query}"
        result = VectorStoreService.search(query=q, k=settings.top_k)
        if not result.strip():
            return "Không tìm thấy dữ liệu điểm chuẩn trong Knowledge Base."
        return result[:settings.max_tool_result_chars]
    except Exception as exc:
        return f"Lỗi tra cứu điểm chuẩn: {exc}"

@tool
def admission_faq(question: str) -> str:
    """Trả lời FAQ tuyển sinh: hồ sơ, thời gian, học phí, phương thức xét tuyển, tổ hợp môn."""
    try:
        q = f"FAQ tuyển sinh hồ sơ thời gian học phí phương thức tổ hợp môn {question}"
        result = VectorStoreService.search(query=q, k=settings.top_k)
        if not result.strip():
            return "Không tìm thấy FAQ phù hợp trong Knowledge Base."
        return result[:settings.max_tool_result_chars]
    except Exception as exc:
        return f"Lỗi FAQ: {exc}"
