from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

"""
请求示例1:
http://localhost:8000/portal?teleport=true
响应示例1:
HTTP/1.1 307 Temporary Redirect
Location: https://www.youtube.com/watch?v=dQw4w9WgXc

请求示例2:
http://localhost:8000/portal
响应示例2:
{
    "message": "Here's your interdimensional portal."
} 
"""