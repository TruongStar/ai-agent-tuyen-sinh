from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Tìm kiếm web khi thông tin không có trong PDF hoặc cần dữ liệu mới."""
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        return search.run(query)
    except Exception as exc:
        return (
            "Web search không khả dụng trong môi trường hiện tại. "
            f"Lỗi: {exc}"
        )
