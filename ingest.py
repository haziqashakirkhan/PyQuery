from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = str(BASE_DIR / "chroma_db")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def extract_pdf_text(pdf_path):

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        raise ValueError(f"{pdf_path.name} is not a valid PDF file.") from exc

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text
        })

    if not pages or not any(page["text"].strip() for page in pages):
        raise ValueError(
            f"{pdf_path.name} does not contain readable text. "
            "Please upload real PDF study notes."
        )

    return pages


def main():

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))


    if len(pdf_files) != 5:

        raise ValueError(
            f"Expected exactly 5 PDF files in data/, "
            f"but found {len(pdf_files)}."
        )


    print("\nFound PDFs:")

    for pdf in pdf_files:
        print(f" - {pdf.name}")


    client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )


    try:
        client.delete_collection("python_notes")
    except Exception:
        pass


    collection = client.create_collection(
        name="python_notes"
    )


    documents = []
    metadatas = []
    ids = []


    counter = 0


    print("\nExtracting text and creating chunks...\n")


    for pdf_path in pdf_files:

        pages = extract_pdf_text(pdf_path)


        for page_data in pages:

            chunks = chunk_text(
                page_data["text"]
            )


            for chunk in chunks:

                documents.append(chunk)

                metadatas.append({
                    "source": pdf_path.name,
                    "page": page_data["page"]
                })

                ids.append(
                    f"chunk_{counter}"
                )

                counter += 1


    print(f"Total chunks: {len(documents)}")

    print("Generating embeddings...")


    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    ).tolist()


    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


    print("\n--------------------------------")
    print("PyQuery study index created.")
    print("--------------------------------")
    print(f"PDFs: {len(pdf_files)}")
    print(f"Chunks: {len(documents)}")
    print(f"Vector database: {CHROMA_DIR}")
    print("--------------------------------")


if __name__ == "__main__":
    main()