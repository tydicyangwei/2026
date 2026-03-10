import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatMessage(BaseModel):
    history: List[Message]
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float = Field(default=1.0)

@app.post("/v1/chat/completions")
async def create_chat_response(message: ChatMessage):
    return {"message": "Hello World"}

if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=6006, log_level="info", workers=1)
