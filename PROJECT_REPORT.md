# Báo Cáo Mô Tả Hệ Thống AI Agent Tuyển Sinh

## 1. Mục tiêu

Xây dựng hệ thống AI Agent hỗ trợ tư vấn tuyển sinh đại học, có khả năng trả lời câu hỏi dựa trên tài liệu PDF, gợi ý ngành học, tra cứu điểm chuẩn và sử dụng nhiều công cụ hỗ trợ.

## 2. Vấn đề cần giải quyết

Các thí sinh thường gặp khó khăn khi tìm kiếm thông tin tuyển sinh do dữ liệu phân tán trong nhiều file PDF, website hoặc thông báo. Chatbot thông thường dễ trả lời sai nếu không có dữ liệu nền. Vì vậy hệ thống cần một AI Agent có khả năng:
- Tìm kiếm tài liệu
- Chọn công cụ phù hợp
- Suy luận theo ngữ cảnh
- Trả lời có căn cứ

## 3. Công nghệ sử dụng

- Python
- Streamlit
- LangChain
- LangGraph
- FAISS
- OpenAI GPT-4o
- Google Gemini
- PyPDF
- DuckDuckGo Search

## 4. Kiến trúc hệ thống

Hệ thống gồm 4 lớp:

### 4.1 UI Layer
Giao diện Streamlit cho phép:
- Chat với Agent
- Upload PDF
- Rebuild Knowledge Base
- Xem tool logs
- Xem kiến trúc

### 4.2 Agent Layer
AgentController quản lý:
- LLM
- Tools
- Memory
- Workflow
- Streaming events

### 4.3 Tool Layer
Bao gồm:
- search_knowledge_base
- lookup_admission_score
- recommend_major
- admission_faq
- calculator
- web_search

### 4.4 Data Layer
Bao gồm:
- PDF files
- FAISS vectorstore
- Chat history JSON
- Logs

## 5. Quy trình xử lý

1. Người dùng đặt câu hỏi.
2. Agent nhận câu hỏi.
3. LLM phân tích cần dùng tool nào.
4. Agent gọi tool.
5. Tool trả kết quả.
6. Agent tổng hợp câu trả lời.
7. UI hiển thị kết quả và tool logs.

## 6. Điểm khác biệt so với chatbot

Chatbot thường:
- Chỉ nhận câu hỏi và trả lời.
- Không có tool.
- Không có observation.
- Không có workflow.

AI Agent trong hệ thống:
- Có ReAct workflow.
- Có tool calling.
- Có memory.
- Có RAG.
- Có logging.
- Có khả năng chọn hành động.

## 7. Hướng phát triển

- Thêm database PostgreSQL
- Thêm authentication
- Thêm API backend FastAPI
- Thêm Docker
- Thêm đánh giá độ chính xác
- Thêm citation chi tiết
- Thêm dashboard admin
