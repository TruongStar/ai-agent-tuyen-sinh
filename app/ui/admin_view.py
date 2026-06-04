# app/ui/admin_view.py
# Giao diện dành cho quản trị viên dữ liệu

from pathlib import Path
import shutil
import streamlit as st

PDF_DIR = Path("data/pdfs")
VECTOR_DIR = Path("data/vectorstore")
LOG_DIR = Path("data/logs")


def render_admin_view(rebuild_kb_func=None):
    st.title("🛠️ Quản trị hệ thống AI Agent ICTU")
    st.caption("Quản lý PDF Knowledge Base, rebuild vectorstore, kiểm tra log và trạng thái dữ liệu")

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    tabs = st.tabs(["📚 Knowledge Base", "🔁 Rebuild KB", "📜 Logs", "⚙️ Cấu hình"])

    with tabs[0]:
        st.subheader("📚 Danh sách PDF hiện có")
        pdf_files = sorted(PDF_DIR.glob("*.pdf"))
        if pdf_files:
            for file in pdf_files:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• {file.name}")
                with col2:
                    if st.button("Xóa", key=f"delete_{file.name}"):
                        file.unlink(missing_ok=True)
                        st.success(f"Đã xóa {file.name}")
                        st.rerun()
        else:
            st.info("Chưa có PDF nào trong data/pdfs.")

        st.divider()
        st.subheader("⬆️ Upload PDF mới")
        uploaded_files = st.file_uploader(
            "Chọn một hoặc nhiều file PDF",
            type=["pdf"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            for uploaded in uploaded_files:
                save_path = PDF_DIR / uploaded.name
                with open(save_path, "wb") as f:
                    f.write(uploaded.getbuffer())
            st.success(f"Đã upload {len(uploaded_files)} file PDF.")

    with tabs[1]:
        st.subheader("🔁 Rebuild Knowledge Base")
        st.write("Bấm nút dưới để tạo lại vectorstore sau khi thêm/xóa PDF.")

        if st.button("Rebuild KB", type="primary"):
            with st.spinner("Đang rebuild Knowledge Base..."):
                if rebuild_kb_func is not None:
                    try:
                        result = rebuild_kb_func()
                        st.success("Rebuild KB thành công.")
                        if result:
                            st.write(result)
                    except Exception as e:
                        st.error(f"Rebuild KB lỗi: {e}")
                else:
                    st.warning("Chưa truyền hàm rebuild_kb_func. Hãy kết nối với service build vectorstore của bạn.")

        if st.button("Reset vectorstore"):
            if VECTOR_DIR.exists():
                shutil.rmtree(VECTOR_DIR)
            VECTOR_DIR.mkdir(parents=True, exist_ok=True)
            st.success("Đã reset vectorstore.")

    with tabs[2]:
        st.subheader("📜 Log hệ thống")
        log_files = sorted(LOG_DIR.glob("*.log"), reverse=True)
        if log_files:
            selected_log = st.selectbox("Chọn file log", [x.name for x in log_files])
            log_path = LOG_DIR / selected_log
            content = log_path.read_text(encoding="utf-8", errors="ignore")
            st.text_area("Nội dung log", content[-10000:], height=400)
        else:
            st.info("Chưa có file log.")

    with tabs[3]:
        st.subheader("⚙️ Cấu hình Agent")
        provider = st.selectbox("Provider", ["openai", "gemini", "local"], index=0)
        model = st.text_input("Model", value="gpt-4o-mini")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
        st.session_state.admin_config = {
            "provider": provider,
            "model": model,
            "temperature": temperature,
        }
        st.json(st.session_state.admin_config)
