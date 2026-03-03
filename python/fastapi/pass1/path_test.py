# -*- coding: utf-8 -*-
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def hello():
    return {"message": "Hello World"}
@app.get("/hello2/{name}")
async def hello2(name: str):
    return {"message": f"Hello {name}"}
