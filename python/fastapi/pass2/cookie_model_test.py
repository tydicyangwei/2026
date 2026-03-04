from typing import Annotated
from fastapi import FastAPI, Cookie
from pydantic import BaseModel
app = FastAPI()

class CookieModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    session_id: str | None = None
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/cookie/")
async def read_cookie(cookie: Annotated[CookieModel, Cookie()]):
    return cookie

"""
请求示例：
http://localhost:8000/cookie/?session_id=test_session_id&fatebook_tracker=test_fatebook_tracker&googall_tracker=test_googall_tracker
响应示例：
{
    "session_id": "test_session_id",
    "fatebook_tracker": "test_fatebook_tracker",
    "googall_tracker": "test_googall_tracker"
}
"""
