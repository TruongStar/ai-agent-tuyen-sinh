import json
from pathlib import Path
from datetime import datetime
from app.core.settings import settings

class ChatHistoryStore:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.base_dir = Path(settings.chat_history_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_dir / f"{session_id}.json"

    def load(self):
        if not self.file_path.exists():
            return []
        try:
            return json.loads(self.file_path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def append(self, role: str, content: str):
        data = self.load()
        data.append({
            "role": role,
            "content": content,
            "created_at": datetime.now().isoformat()
        })
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def clear(self):
        if self.file_path.exists():
            self.file_path.unlink()
