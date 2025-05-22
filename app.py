from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import extract_and_index, ask_question

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    answer = ask_question(query.question)
    return {"answer": answer}
