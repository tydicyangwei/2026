from typing import Annotated
from fastapi import FastAPI,Depends
app = FastAPI()

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

"""
请求示例：
http://127.0.0.1:8000/items/?q=fastapi&skip=10&limit=20
响应示例：
{
    "q": "fastapi",
    "skip": 10,
    "limit": 20
}
"""

