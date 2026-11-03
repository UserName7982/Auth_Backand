from typing import List
from pydantic import BaseModel

class ChatRequest(BaseModel):
    text: str