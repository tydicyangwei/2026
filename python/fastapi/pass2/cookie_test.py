from typing import Annotated
from fastapi import FastAPI, Cookie
app = FastAPI()

@app.get("/cookie/")
async def read_cookie(session_id: Annotated[str | None, Cookie()] = None):
    return {"session_id": session_id}

"""
请求示例：
http://localhost:8000/cookie/?session_id=test_session_id
响应示例：
{
    "session_id": "test_session_id"
}
"""