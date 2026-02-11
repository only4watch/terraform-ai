from fastapi import FastAPI
from pydantic import BaseModel
import os

from chunker import chunk_terraform_code
from embeddings import add_chunks_to_db
from rag import ask_terraform_ai

app = FastAPI()


class LocalPathRequest(BaseModel):
    path: str


class QuestionRequest(BaseModel):
    question: str


@app.post("/index/local")
def index_local(request: LocalPathRequest):
    try:
        folder_path = request.path

        if not os.path.exists(folder_path):
            return {"error": "Folder path does not exist"}

        all_chunks = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".tf"):
                    full_path = os.path.join(root, file)

                    with open(full_path, "r", encoding="utf-8") as f:
                        tf_text = f.read()

                    chunks = chunk_terraform_code(tf_text)
                    all_chunks.extend(chunks)

        if not all_chunks:
            return {"error": "No .tf files found in folder"}

        print("Total chunks:", len(all_chunks))

        add_chunks_to_db(all_chunks)

        return {"message": "Local Terraform folder indexed successfully"}

    except Exception as e:
        return {"error": str(e)}


@app.post("/ask")
def ask(request: QuestionRequest):
    try:
        answer = ask_terraform_ai(request.question)
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def health():
    return {"status": "Terraform AI is running"}
