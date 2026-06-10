from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.data.data import load_from_csv, load_from_api, get_stats, get_metadata, get_df
from app.data.summary import QueryInput
from app.chain.steps import PromptBuilder, LLMRunner, ResponseParser
from app.config import settings
chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chain
    chain = PromptBuilder() | LLMRunner() | ResponseParser()
    yield

app = FastAPI(lifespan=lifespan)

class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/data/upload")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="För stor fil")
    try:
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

@app.post("/ai/ask")
def ask(body: AskRequest):
    try:
        df = get_df()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        result = chain.run(QueryInput(question=body.question, df=df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Modellfel: {e}")
    return result.model_dump()