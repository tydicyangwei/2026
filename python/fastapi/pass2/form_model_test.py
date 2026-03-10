from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel
app = FastAPI()

class LoginForm(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(form_data: Annotated[LoginForm, Form()]):
    return {"username": form_data.username}
