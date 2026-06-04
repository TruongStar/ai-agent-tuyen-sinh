# AI Agent Tư Vấn Tuyển Sinh Đại Học


## Thành phần chính

- LangGraph ReAct Agent
- Agent Controller
- Tool Registry
- Tool Calling Realtime
- Memory theo session
- RAG PDF với FAISS
- Upload PDF trực tiếp trong giao diện
- Rebuild / Reset Knowledge Base
- Citation nguồn từ PDF
- GPT-4o hoặc Gemini
- Web Search
- Calculator
- Intent Analyzer
- Major Recommender
- Admission Score Lookup
- FAQ Tool
- Chat History lưu local JSON
- Logging
- Error Handling
- Streamlit UI nhiều tab


## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu hình API key

Copy file:

```bash
copy .env.example .env
```

Sau đó sửa:

```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

GOOGLE_API_KEY=...
GEMINI_MODEL=gemini-1.5-pro
```

## Chạy

```bash
streamlit run main.py
```

## Thêm dữ liệu PDF

Có 2 cách:

1. Upload trực tiếp trên giao diện.
2. Copy PDF vào thư mục:

```text
data/pdfs/
```

Sau đó bấm **Rebuild Knowledge Base**.

## Kiến trúc

```text
User
 ↓
Streamlit UI
 ↓
AgentController
 ↓
Intent Analyzer
 ↓
LangGraph ReAct Agent
 ↓
Tool Registry
 ├─ search_knowledge_base
 ├─ lookup_admission_score
 ├─ recommend_major
 ├─ admission_faq
 ├─ calculator
 └─ web_search
 ↓
Observation
 ↓
Final Answer
```

## AI Agent?

Vì hệ thống không chỉ hỏi đáp đơn thuần. Nó có:
- LLM reasoning
- tự chọn tool
- gọi tool
- nhận kết quả tool
- tổng hợp câu trả lời
- memory
- workflow Agent
- logging quan sát được


