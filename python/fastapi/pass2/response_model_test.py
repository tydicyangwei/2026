from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

"""
请求体示例：
{
    "username": "yangwei",
    "password": "str123",
    "email": "111@163.com",
    "full_name": "aaa"
}
响应示例：
{
    "username": "yangwei",
    "email": "111@163.com",
    "full_name": "aaa"
}
"""

