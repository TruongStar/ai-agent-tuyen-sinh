from langchain_core.tools import tool
from app.services.vectorstore_service import VectorStoreService
from app.core.settings import settings

MAJOR_RULES = [
    {
        "keywords": ["lập trình", "code", "python", "java", "c++", "web", "app", "phần mềm"],
        "majors": ["Công nghệ thông tin", "Kỹ thuật phần mềm", "Khoa học máy tính"],
        "reason": "phù hợp với người thích lập trình và xây dựng phần mềm",
    },
    {
        "keywords": ["ai", "trí tuệ nhân tạo", "machine learning", "data", "dữ liệu"],
        "majors": ["Trí tuệ nhân tạo", "Khoa học dữ liệu", "Công nghệ thông tin"],
        "reason": "phù hợp với định hướng AI, dữ liệu và mô hình học máy",
    },
    {
        "keywords": ["mạng", "bảo mật", "an toàn", "cyber", "hacker", "security"],
        "majors": ["An toàn thông tin", "Mạng máy tính và truyền thông dữ liệu"],
        "reason": "phù hợp với bảo mật hệ thống, mạng và an ninh mạng",
    },
    {
        "keywords": ["điện tử", "iot", "robot", "nhúng", "vi mạch", "arduino"],
        "majors": ["Kỹ thuật điện tử viễn thông", "IoT", "Kỹ thuật máy tính"],
        "reason": "phù hợp với phần cứng, thiết bị thông minh và hệ thống nhúng",
    },
    {
        "keywords": ["kinh doanh", "marketing", "bán hàng", "quản trị", "startup"],
        "majors": ["Quản trị kinh doanh", "Thương mại điện tử", "Marketing số"],
        "reason": "phù hợp với định hướng kinh doanh và vận hành doanh nghiệp",
    },
    {
        "keywords": ["thiết kế", "đồ họa", "sáng tạo", "ui", "ux", "media"],
        "majors": ["Thiết kế đồ họa", "Truyền thông đa phương tiện", "UI/UX"],
        "reason": "phù hợp với khả năng sáng tạo, hình ảnh và trải nghiệm người dùng",
    },
]

@tool
def recommend_major(profile: str) -> str:
    """Gợi ý ngành học theo sở thích, điểm số, môn mạnh, tính cách, mục tiêu nghề nghiệp."""
    text = profile.lower()
    matched = []

    for rule in MAJOR_RULES:
        if any(k in text for k in rule["keywords"]):
            matched.append(rule)

    if not matched:
        return (
            "Chưa đủ dữ kiện để gợi ý ngành chính xác. "
            "Hãy cung cấp thêm: điểm dự kiến, môn mạnh, sở thích, nghề mong muốn."
        )

    lines = ["Gợi ý ngành phù hợp:"]
    all_majors = []

    for rule in matched:
        for major in rule["majors"]:
            all_majors.append(major)
            lines.append(f"- {major}: {rule['reason']}.")

    try:
        kb = VectorStoreService.search(" ".join(set(all_majors)), k=settings.top_k)
        lines.append("\nThông tin liên quan từ Knowledge Base:")
        lines.append(kb[:settings.max_tool_result_chars])
    except Exception:
        lines.append("\nChưa tra được PDF Knowledge Base. Đây là gợi ý theo rule nội bộ.")

    return "\n".join(lines)
