from typing import Any, Dict, Generator
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.core.llm_factory import LLMFactory
from app.core.prompts import SYSTEM_PROMPT
from app.core.tool_registry import ToolRegistry
from app.core.logger import logger

_GLOBAL_MEMORY = MemorySaver()

class AgentController:
    """
    Agent Controller chuẩn AI Agent:
    - Khởi tạo LLM
    - Khởi tạo Tool Registry
    - Tạo LangGraph ReAct Agent
    - Quản lý memory bằng thread_id
    - Stream events để UI hiển thị tool đang gọi
    """

    def __init__(
        self,
        provider: str,
        model: str | None,
        temperature: float,
        thread_id: str,
    ):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.thread_id = thread_id

        self.llm = LLMFactory.create(
            provider=provider,
            model=model,
            temperature=temperature,
        )

        self.tools = ToolRegistry.all_tools()

        self.graph = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=_GLOBAL_MEMORY,
            prompt=SYSTEM_PROMPT,
        )

    def _config(self):
        return {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

    def invoke(self, question: str) -> Dict[str, Any]:
        logger.info("Invoke agent: %s", question)
        return self.graph.invoke(
            {"messages": [("user", question)]},
            config=self._config(),
        )

    def stream(self, question: str) -> Generator[dict, None, None]:
        logger.info("Stream agent: %s", question)

        yield {
            "type": "thinking",
            "content": "Agent đang phân tích câu hỏi..."
        }

        final_answer = ""

        try:
            for event in self.graph.stream(
                {"messages": [("user", question)]},
                config=self._config(),
                stream_mode="updates",
            ):
                for node_name, payload in event.items():
                    messages = payload.get("messages", []) if isinstance(payload, dict) else []

                    for msg in messages:
                        msg_type = getattr(msg, "type", "")

                        tool_calls = getattr(msg, "tool_calls", None)
                        if tool_calls:
                            for call in tool_calls:
                                name = call.get("name", "unknown_tool")
                                args = call.get("args", {})
                                logger.info("Tool start: %s | %s", name, args)
                                yield {
                                    "type": "tool_start",
                                    "tool_name": name,
                                    "args": args,
                                    "content": f"Đang gọi tool: {name}",
                                }

                        if msg_type == "tool":
                            tool_name = getattr(msg, "name", "tool")
                            content = getattr(msg, "content", "")
                            logger.info("Tool result: %s", tool_name)
                            yield {
                                "type": "tool_result",
                                "tool_name": tool_name,
                                "content": content,
                            }

                        if msg_type == "ai":
                            content = getattr(msg, "content", "")
                            if content:
                                final_answer = content
                                yield {
                                    "type": "message",
                                    "content": content,
                                }

            yield {
                "type": "final",
                "content": final_answer,
            }

        except Exception as exc:
            logger.exception("Agent error")
            yield {
                "type": "error",
                "content": str(exc),
            }
