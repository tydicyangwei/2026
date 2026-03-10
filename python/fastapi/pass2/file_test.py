from typing import Annotated
from fastapi import FastAPI,File, UploadFile
app = FastAPI()
@app.post("/file/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile, File()]):
    return {"filename": file.filename}

