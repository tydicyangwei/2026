from typing import Annotated
from fastapi import FastAPI, Form
app = FastAPI()
app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
"""
请求体示例：
username=yangwei&password=str123
响应示例：
{
    "username": "yangwei"
}
"""