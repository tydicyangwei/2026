from fastapi import FastAPI, Response

app = FastAPI()

@app.post("/set_cookie")
def set_cookie(response: Response):
    response.set_cookie(key="my_cookie", value="cookie_value")
    return {"message": "Cookie has been set!"}

