from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: str = datetime.now().isoformat()
