from fastapi import FastAPI,Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = "0.001"
    return response

