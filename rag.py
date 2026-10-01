import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the same folder as this file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq


CHROMA_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "python_notes"
TOP_K = 5


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


client = chromadb.PersistentClient(
    path=CHROMA_DIR
)


def get_collection():
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception:
        return client.create_collection(name=COLLECTION_NAME)


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY was not found. "
        "Check the .env file in the PyQuerry folder."
    )


groq_client = Groq(
    api_key=api_key
)


MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)
MODEL_CANDIDATES = [
    MODEL,
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b",
]


def retrieve(question):

    question_embedding = embedding_model.encode(
        [question]
    ).tolist()[0]

    collection = get_collection()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K
    )


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]


    return documents, metadatas


def ask_question(question):

    documents, metadatas = retrieve(question)

    if not documents:
        return {
            "answer": "The answer is not available in the uploaded documents.",
            "sources": []
        }


    context_parts = []


    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"""
Source: {metadata.get("source")}
Page: {metadata.get("page")}

{document}
"""
        )


    context = "\n\n".join(context_parts)


    prompt = f"""
You are PyQuery, an AI Study Assistant for
Python programming students.

Answer the user's question using ONLY the
provided study material.

If the answer cannot be found in the provided
context, say exactly:

"The answer is not available in the uploaded documents."

Do not invent information.

Explain the answer clearly and simply.

Study material:

{context}

User question:

{question}
"""

    last_error = None
    for model_name in dict.fromkeys(MODEL_CANDIDATES):
        try:
            response = groq_client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You answer questions using "
                            "retrieved Python study notes."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
            answer = response.choices[0].message.content
            break
        except Exception as exc:
            last_error = exc
            continue
    else:
        if last_error is not None:
            raise RuntimeError(f"Groq model request failed: {last_error}") from last_error
        raise RuntimeError("No Groq model was available for this request.")

    sources = []


    for metadata, document in zip(
        metadatas,
        documents
    ):

        sources.append({
            "file": metadata.get("source"),
            "page": metadata.get("page"),
            "text": document
        })

    return {
        "answer": answer,
        "sources": sources
    }