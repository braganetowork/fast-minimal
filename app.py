from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
