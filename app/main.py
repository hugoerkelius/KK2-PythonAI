from fastapi import FastAPI, UploadFile, File, HTTPException
from app.data.data import load_from_csv, load_from_api, get_stats, get_metadata

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/data/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        load_from_csv(contents, file.filename)
        return get_metadata()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/data/load_api")
def load_api():
    try:
        load_from_api()
        return get_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/stats")
def stats():
    try:
        return get_stats()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))