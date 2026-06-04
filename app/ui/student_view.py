# app/ui/student_view.py
# Giao diện dành cho sinh viên/thí sinh

import streamlit as st


def render_student_view(agent=None):
    st.title("🎓 Cổng tư vấn tuyển sinh ICTU")
    st.caption("Hỏi đáp ngành học, điểm chuẩn, học phí, phương thức xét tuyển, biểu mẫu và cơ hội nghề nghiệp")

    with st.sidebar:
        st.subheader("👤 Sinh viên / Thí sinh")
        st.write("Bạn có thể hỏi về:")
        st.markdown("""
        - Ngành đào tạo
        - Điểm chuẩn
        - Học phí
        - Tổ hợp xét tuyển
        - Phương thức tuyển sinh
        - Biểu mẫu sinh viên
        - Cơ hội việc làm
        """)

    tabs = st.tabs(["💬 Hỏi đáp", "📚 Câu hỏi mẫu", "📄 Biểu mẫu"])

    with tabs[0]:
        question = st.chat_input("Nhập câu hỏi tuyển sinh...")
        if "student_messages" not in st.session_state:
            st.session_state.student_messages = []

        for msg in st.session_state.student_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if question:
            st.session_state.student_messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Agent đang tìm thông tin..."):
                    if agent is not None:
                        try:
                            answer = agent.run(question)
                        except AttributeError:
                            answer = agent.invoke(question)
                        except Exception as e:
                            answer = f"Có lỗi khi gọi Agent: {e}"
                    else:
                        answer = "Chưa kết nối Agent. Hãy truyền agent vào hàm render_student_view(agent)."
                    st.markdown(answer)
                    st.session_state.student_messages.append({"role": "assistant", "content": answer})

    with tabs[1]:
        st.subheader("📚 Câu hỏi mẫu")
        sample_questions = [
            "ICTU năm 2026 có những ngành nào?",
            "Ngành Công nghệ thông tin xét tổ hợp nào?",
            "Học phí ngành CNTT khoảng bao nhiêu?",
            "Điểm chuẩn ICTU năm 2025 là bao nhiêu?",
            "Em thích lập trình thì nên chọn ngành nào?",
            "Cho tôi link Giấy xác nhận sinh viên",
            "ICTU có doanh nghiệp nào hợp tác tuyển dụng?",
        ]
        for q in sample_questions:
            st.code(q, language="text")

    with tabs[2]:
        st.subheader("📄 Tra cứu biểu mẫu")
        form_name = st.text_input("Nhập tên biểu mẫu", placeholder="Ví dụ: giấy xác nhận sinh viên")
        if st.button("Tìm biểu mẫu"):
            if not form_name.strip():
                st.warning("Vui lòng nhập tên biểu mẫu cần tìm.")
            else:
                query = f"Cho tôi link biểu mẫu: {form_name}"
                if agent is not None:
                    try:
                        answer = agent.run(query)
                    except AttributeError:
                        answer = agent.invoke(query)
                    except Exception as e:
                        answer = f"Có lỗi khi gọi Agent: {e}"
                else:
                    answer = "Chưa kết nối Agent."
                st.markdown(answer)
