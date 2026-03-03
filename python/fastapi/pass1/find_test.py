from fastapi import FastAPI
app = FastAPI()
@app.get("/find/")
async def find(q: str, limit: int = 10):
    return {"message": f"You searched for {q} with limit {limit}"}