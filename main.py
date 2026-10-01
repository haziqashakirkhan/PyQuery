import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

from rag import ask_question


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


app = FastAPI(
    title="PyQuery",
    description="AI Study Assistant using RAG"
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    exist_ok=True
)


class QuestionRequest(BaseModel):

    question: str


@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.post("/upload")
async def upload_pdfs(
    files: list[UploadFile] = File(...)
):

    if len(files) != 5:

        return {
            "error": "Please upload exactly 5 PDF files."
        }


    for old_file in DATA_DIR.glob("*.pdf"):
        try:
            old_file.unlink()
        except PermissionError:
            # Windows may lock a PDF that is already open in another app.
            # Skip that file instead of crashing the upload request.
            continue


    for file in files:

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            continue

        file_path = DATA_DIR / file.filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except PermissionError:
            return {
                "error": f"The file '{file.filename}' is open in another program. Close it and try again."
            }

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if len(pdf_files) != 5:
        return {
            "error": "Please upload exactly 5 valid PDF files."
        }


    # Run ingestion after upload
    import subprocess
    import sys

    venv_python = BASE_DIR / ".venv" / "Scripts" / "python.exe"
    python_exec = str(venv_python) if venv_python.exists() else sys.executable

    try:
        result = subprocess.run(
            [python_exec, str(BASE_DIR / "ingest.py")],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True
        )
    except Exception as exc:
        return {
            "error": "Failed to run study indexing process.",
            "details": str(exc)
        }


    if result.returncode != 0:

        error_detail = (result.stderr or result.stdout or "Unknown PDF parsing error").strip()

        return {
            "error": "Failed to create study index.",
            "details": error_detail
        }


    return {
        "message": "Study index created successfully.",
        "chunks": get_chunk_count()
    }


def get_chunk_count():

    try:

        import chromadb

        client = chromadb.PersistentClient(
            path=str(BASE_DIR / "chroma_db")
        )

        collection = client.get_collection(
            "python_notes"
        )

        return collection.count()

    except Exception:

        return 0


@app.post("/ask")
async def ask(request: QuestionRequest):

    if not request.question.strip():

        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    try:
        result = ask_question(
            request.question
        )
    except Exception as exc:
        return {
            "answer": f"The answer is not available in the uploaded documents. Details: {exc}",
            "sources": []
        }


    return result