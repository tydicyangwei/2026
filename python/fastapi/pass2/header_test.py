from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}

"""
请求示例：
curl -X 'GET' \ 
    'http://localhost:8000/items/' \
    -H 'X-Token: test_token1' \
    -H 'X-Token: test_token2' 
响应示例：
{   
    "X-Token values": [
        "test_token1",
        "test_token2"  
    ]
}
"""