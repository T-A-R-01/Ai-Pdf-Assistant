from fastapi import FastAPI, File, UploadFile

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from rag_pipeline import (
    extract_text_from_pdf,
    split_text_into_chunks,
    create_vector_store,
    answer_user_question
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI PDF Assistant Backend Running"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    text = extract_text_from_pdf(file.file)

    chunks = split_text_into_chunks(text)

    create_vector_store(chunks)

    return {"message": "PDF processed successfully"}

class QuestionRequest(BaseModel):
    question: str
    
@app.post("/ask")
async def ask_question(request: QuestionRequest):

    response = answer_user_question(request.question)

    return {"answer": response}