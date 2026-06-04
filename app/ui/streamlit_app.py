import uuid
import streamlit as st

from app.core.settings import settings
from app.core.agent_controller import AgentController
from app.core.tool_registry import ToolRegistry
from app.services.pdf_service import PDFService
from app.services.vectorstore_service import VectorStoreService
from app.storage.history_store import ChatHistoryStore
from app.ui.components import render_tool_event, render_architecture

def init_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "tool_events" not in st.session_state:
        st.session_state.tool_events = []

def sidebar_config():
    with st.sidebar:
        st.header("⚙️ Agent Config")

        provider = st.selectbox(
            "Provider",
            ["openai", "gemini"],
            index=0 if settings.model_provider == "openai" else 1
        )

        default_model = settings.openai_model if provider == "openai" else settings.gemini_model

        model = st.text_input("Model", value=default_model)

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=float(settings.temperature),
            step=0.1
        )

        st.divider()
        st.header("📚 Knowledge Base")

        uploads = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploads:
            saved = PDFService.save_uploaded_files(uploads)
            st.success(f"Đã lưu {len(saved)} file PDF.")

        pdfs = PDFService.list_pdfs()

        if pdfs:
            st.caption("PDF hiện có:")
            for p in pdfs:
                st.write(f"• {p.name}")
        else:
            st.warning("Chưa có PDF.")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Rebuild KB", use_container_width=True):
                try:
                    with st.spinner("Đang build FAISS vector DB..."):
                        info = VectorStoreService.build(provider=provider)
                    st.success(f"{info['pdf_count']} PDF | {info['chunk_count']} chunks")
                except Exception as exc:
                    st.error(str(exc))

        with col_b:
            if st.button("Reset KB", use_container_width=True):
                VectorStoreService.reset()
                st.success("Đã reset.")

        st.divider()
        st.header("🧠 Session")

        if st.button("Xoá chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.tool_events = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

        return provider, model, temperature

def run_app():
    st.set_page_config(
        page_title="AI Agent Tuyển Sinh",
        page_icon="🎓",
        layout="wide"
    )

    init_state()

    provider, model, temperature = sidebar_config()

    st.title("🎓 AI Agent Hỗ Trợ Tư Vấn Tuyển Sinh Đại Học")
    st.caption("LangGraph + ReAct + Tool Calling + RAG PDF + GPT-4o/Gemini + Memory")

    tab_chat, tab_tools, tab_kb, tab_arch = st.tabs([
        "💬 Chat",
        "🛠️ Tool Logs",
        "📚 Knowledge Base",
        "🏗️ Kiến trúc"
    ])

    history = ChatHistoryStore(st.session_state.session_id)

    with tab_chat:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        question = st.chat_input("Nhập câu hỏi tuyển sinh...")

        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            history.append("user", question)

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                status = st.empty()
                tool_area = st.container()
                answer_area = st.empty()

                controller = AgentController(
                    provider=provider,
                    model=model,
                    temperature=temperature,
                    thread_id=st.session_state.session_id,
                )

                final_answer = ""

                for event in controller.stream(question):
                    if event["type"] in ["thinking", "tool_start", "tool_result"]:
                        st.session_state.tool_events.append(event)
                        with tool_area:
                            render_tool_event(event)

                    elif event["type"] == "message":
                        final_answer = event["content"]
                        answer_area.markdown(final_answer)

                    elif event["type"] == "final":
                        final_answer = event["content"] or final_answer
                        status.success("✅ Agent hoàn thành.")

                    elif event["type"] == "error":
                        status.error("Agent lỗi.")
                        st.error(event["content"])

                if not final_answer:
                    final_answer = "Agent chưa tạo được câu trả lời cuối cùng."

                answer_area.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                history.append("assistant", final_answer)

    with tab_tools:
        st.subheader("🛠️ Tool logs realtime")
        if not st.session_state.tool_events:
            st.info("Chưa có tool nào được gọi.")
        else:
            for event in st.session_state.tool_events:
                render_tool_event(event)

        st.subheader("Tools đã đăng ký")
        for name in ToolRegistry.tool_names():
            st.code(name)

    with tab_kb:
        st.subheader("📚 PDF Knowledge Base")
        pdfs = PDFService.list_pdfs()
        st.write(f"Số PDF: {len(pdfs)}")
        st.write("Vector DB:", "✅ Đã có" if VectorStoreService.exists() else "❌ Chưa build")

        for p in pdfs:
            st.write(f"- {p.name}")

        st.info("Muốn đổi dữ liệu: xoá PDF cũ trong data/pdfs hoặc upload PDF mới, sau đó bấm Rebuild KB.")

    with tab_arch:
        st.subheader("🏗️ Kiến trúc hệ thống")
        render_architecture()

        st.markdown(
            """
### Luồng xử lý

1. Người dùng nhập câu hỏi.
2. AgentController gửi câu hỏi vào LangGraph.
3. LLM phân tích ý định.
4. Agent tự chọn tool phù hợp.
5. Tool trả observation.
6. LLM tổng hợp câu trả lời cuối cùng.
7. UI hiển thị tool đang gọi và kết quả.

### Đây là AI Agent vì có:

- Reasoning
- Tool calling
- Observation
- Memory
- Workflow
- Knowledge Base
- Logging
- Multi-model support
            """
        )
