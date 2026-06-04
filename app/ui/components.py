import streamlit as st

def render_metric_card(label: str, value: str):
    st.metric(label, value)

def render_tool_event(event: dict):
    if event["type"] == "tool_start":
        st.info(f"🔧 Đang gọi tool: `{event.get('tool_name')}`")
        args = event.get("args")
        if args:
            with st.expander("Tham số tool"):
                st.json(args)

    elif event["type"] == "tool_result":
        with st.expander(f"✅ Kết quả tool `{event.get('tool_name')}`"):
            st.write(event.get("content", "")[:5000])

    elif event["type"] == "thinking":
        st.caption("🧠 " + event.get("content", ""))

def render_architecture():
    st.code(
        '''
User
 ↓
Streamlit UI
 ↓
AgentController
 ↓
LangGraph ReAct Agent
 ↓
LLM Reasoning
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
Observation
 ↓
Final Answer
        ''',
        language="text"
    )
