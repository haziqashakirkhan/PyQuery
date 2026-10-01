# PyQuery — AI Study Assistant using RAG

PyQuery is an AI-powered study assistant built using **Retrieval-Augmented Generation (RAG)**. It allows students to ask questions about Python programming and receive answers based specifically on information retrieved from a collection of Python study chapters.

The project combines **PDF text extraction, text chunking, embeddings, ChromaDB vector search, FastAPI, and Groq/Grok LLMs** to create a complete local RAG pipeline.

---

## Project Overview

The goal of PyQuery is to build an AI Study Assistant that can answer questions from **5 Python programming PDF chapters**.

Instead of sending a question directly to an AI model, PyQuery first searches the local knowledge base for relevant information. The retrieved content is then provided to the Groq LLM as context so that the generated answer is grounded in the uploaded study material.

### RAG Pipeline

```text
Python PDF Chapters
        ↓
   Text Extraction
        ↓
    Text Chunking
        ↓
    Embeddings
        ↓
     ChromaDB
        ↓
    User Question
        ↓
   Similarity Search
        ↓
 Relevant Study Chunks
        ↓
      Groq LLM
        ↓
   Final Answer
````

---

## Features

* Upload and process 5 Python PDF chapters
* Extract text from PDF files
* Automatically split extracted text into smaller chunks
* Generate vector embeddings using Sentence Transformers
* Store embeddings locally using ChromaDB
* Retrieve relevant information using semantic similarity search
* Generate answers using Groq's LLM API
* FastAPI backend
* Responsive web interface
* Display retrieved source chapters
* Local vector database
* Environment-variable based API key management
* Simple and student-friendly interface

---

## Technologies Used

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* Python Dotenv

### RAG

* PyPDF
* Sentence Transformers
* ChromaDB
* Vector Embeddings
* Semantic Similarity Search

### AI Model

* Groq API
* `llama-3.3-70b-versatile`

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

---

## Project Structure

```text
PyQuerry/
│
├── data/
│   ├── chapter_1_introduction.pdf
│   ├── chapter_2_variables.pdf
│   ├── chapter_3_conditionals.pdf
│   ├── chapter_4_loops.pdf
│   └── chapter_5_functions.pdf
│
├── chroma_db/
│   └── Local ChromaDB vector database
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── main.py
├── ingest.py
├── rag.py
├── create_pdfs.py
├── requirements.txt
├── .env
└── .gitignore
```

---

# Python Study Chapters

The knowledge base contains five Python programming chapters:

### Chapter 1 — Introduction to Python

Covers:

* What Python is
* Features of Python
* Python syntax
* Basic programming concepts
* Python's uses
* Running Python programs

### Chapter 2 — Variables, Data Types and Operators

Covers:

* Variables
* Variable naming
* Strings
* Integers
* Floats
* Booleans
* Lists
* Tuples
* Dictionaries
* Arithmetic operators
* Comparison operators
* Logical operators
* Assignment operators

### Chapter 3 — Conditional Statements

Covers:

* `if`
* `else`
* `elif`
* Nested conditions
* Comparison operators
* Logical conditions
* Decision-making in Python

### Chapter 4 — Loops and Iteration

Covers:

* `for` loops
* `while` loops
* `range()`
* Nested loops
* `break`
* `continue`
* Iteration

### Chapter 5 — Functions in Python

Covers:

* Defining functions
* Calling functions
* Parameters
* Arguments
* Return values
* Default parameters
* Function scope
* Reusable code

---

# How RAG Works in PyQuery

PyQuery follows a standard Retrieval-Augmented Generation architecture.

## 1. PDF Upload

The user uploads five Python programming PDF chapters through the web interface.

The files are stored inside:

```text
data/
```

---

## 2. Text Extraction

The `ingest.py` script uses **PyPDF** to extract text from each PDF.

```python
PdfReader(pdf_path)
```

The extracted text from all five chapters is combined into the knowledge base.

---

## 3. Text Chunking

Large documents are divided into smaller pieces called chunks.

Chunking makes it easier for the embedding model and vector database to search for specific pieces of information.

Example:

```text
Python is a high-level programming language...
```

may become a searchable chunk containing a smaller section of the original chapter.

---

## 4. Embedding Generation

Each text chunk is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding represents the semantic meaning of the text.

This allows PyQuery to search for information based on meaning instead of only matching exact keywords.

---

## 5. Vector Storage

The generated embeddings are stored locally using **ChromaDB**.

The collection used by the project is:

```text
python_notes
```

The local database is stored inside:

```text
chroma_db/
```

---

## 6. Question Retrieval

When the user asks a question, PyQuery converts the question into an embedding.

For example:

```text
What is a Python variable?
```

The vector database searches for the most semantically relevant chunks from the five chapters.

The system retrieves the top relevant results.

---

## 7. Groq LLM Generation

The retrieved chunks are passed to the Groq API together with the user's question.

The model is instructed to answer using the retrieved study material.

Default model:

```text
llama-3.3-70b-versatile
```

---

## 8. Final Answer

The generated response is returned to the FastAPI backend and displayed in the web interface.

Relevant source information is also shown so the user can identify which chapter was used.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PyQuery.git
```

Move into the project directory:

```bash
cd PyQuery
```

---

## 2. Create a Virtual Environment

It is recommended to use Python 3.10 for this project.

Create the environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root project directory.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Replace:

```text
your_groq_api_key
```

with your actual Groq API key.

### Important

Never upload your `.env` file or API key to GitHub.

The project includes `.env` in `.gitignore`.

---

# Creating the Vector Database

Before running the application for the first time, process the five PDF chapters.

Run:

```bash
python ingest.py
```

The script will:

1. Find the PDF files inside `data/`
2. Extract text
3. Create chunks
4. Generate embeddings
5. Create the ChromaDB collection
6. Store the vectors locally

Expected output will look similar to:

```text
Found PDFs:

- chapter_1_introduction.pdf
- chapter_2_variables.pdf
- chapter_3_conditionals.pdf
- chapter_4_loops.pdf
- chapter_5_functions.pdf

Extracting text and creating chunks...

Total chunks: 23

Generating embeddings...

PyQuery study index created.

PDFs: 5
Chunks: 23
Vector database: chroma_db
```

The exact number of chunks may vary depending on the PDF content and chunking configuration.

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Open the address in your browser.

---

# API Endpoints

## GET `/`

Loads the PyQuery web interface.

```text
GET /
```

---

## POST `/upload`

Uploads and processes the five PDF chapters.

```text
POST /upload
```

The endpoint saves the PDFs and runs the ingestion process.

---

## POST `/ask`

Receives a question and performs the RAG pipeline.

```text
POST /ask
```

Example request:

```json
{
  "question": "What is the difference between a for loop and a while loop?"
}
```

The endpoint retrieves relevant chunks and sends them to the Groq model.

---

# Example Questions

The following questions can be used to test PyQuery.

### Question 1

```text
What is a variable in Python?
```

### Question 2

```text
What is the difference between if, elif and else?
```

### Question 3

```text
What is the difference between a for loop and a while loop?
```

### Additional Questions

```text
What are Python data types?
```

```text
What does the range() function do?
```

```text
What is the purpose of a return statement?
```

```text
What are function parameters?
```

```text
What is a nested conditional statement?
```

---

# Example RAG Process

Suppose the user asks:

```text
What is a while loop?
```

PyQuery does not immediately send the question to the LLM.

Instead:

```text
Question
   ↓
Create Question Embedding
   ↓
Search ChromaDB
   ↓
Find Relevant Loop Chunks
   ↓
Retrieve Context
   ↓
Send Context + Question to Groq
   ↓
Generate Answer
```

This helps the model answer using the information contained in the Python study material.

---

# Why Use RAG?

A general-purpose LLM may generate an answer using information from its training data.

RAG adds an additional retrieval step.

Instead of:

```text
Question → LLM → Answer
```

PyQuery uses:

```text
Question
    ↓
Retrieve Relevant Information
    ↓
Context + Question
    ↓
LLM
    ↓
Answer
```

This makes the application suitable for document-based question answering.

---

# Embedding Model

PyQuery uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model converts text into numerical vector representations.

For example:

```text
"What is a Python variable?"
```

is converted into an embedding vector.

The same process is applied to every knowledge-base chunk.

The vectors can then be compared to determine which chunks are semantically similar to the question.

---

# Vector Database

PyQuery uses **ChromaDB** as its local vector database.

Collection:

```text
python_notes
```

Database directory:

```text
chroma_db/
```

The database stores:

* Text chunks
* Embeddings
* Metadata
* Source information

This allows PyQuery to retrieve relevant study material when a question is submitted.

---

# Backend Architecture

The backend is divided into separate responsibilities.

## `main.py`

Responsible for:

* FastAPI application
* Web routes
* PDF upload
* Serving HTML
* Connecting frontend requests with the RAG system

## `ingest.py`

Responsible for:

* Reading PDFs
* Extracting text
* Chunking documents
* Generating embeddings
* Creating the ChromaDB vector database

## `rag.py`

Responsible for:

* Loading embeddings
* Connecting to ChromaDB
* Retrieving relevant chunks
* Connecting to Groq
* Generating final answers

---

# Frontend

The frontend contains three main sections:

### Study Material

Displays the five Python chapters used as the knowledge base.

### Upload

Allows the five PDF chapters to be uploaded and processed.

### Ask PyQuery

Allows the student to enter a Python-related question and receive an AI-generated answer.

The interface also displays retrieved source information.

---

# Requirements

The main dependencies are:

```text
fastapi
uvicorn
python-multipart
jinja2
python-dotenv
pypdf
chromadb
sentence-transformers
groq
torch
```

Install them with:

```bash
pip install -r requirements.txt
```

---

# Security

The Groq API key is stored in an environment variable.

```env
GROQ_API_KEY=your_api_key
```

The `.env` file should never be committed to GitHub.

The following files/directories are ignored:

```text
.env
.venv/
__pycache__/
*.pyc
chroma_db/
data/*.pdf
```

---

# Limitations

PyQuery is designed specifically around the five Python programming chapters included in the knowledge base.

The quality of an answer depends on:

* Quality of the uploaded PDFs
* Extracted text
* Chunking
* Embedding quality
* Retrieved context
* LLM response

If the required information is not present in the uploaded study material, the system may not be able to provide a reliable document-based answer.

The application also requires an active Groq API key for answer generation.

---

# Future Improvements

Possible improvements include:

* Support for more than five PDFs
* Automatic document management
* Better chunking strategies
* Reranking retrieved documents
* Conversation history
* Streaming AI responses
* Authentication
* Persistent cloud vector database
* Multiple subject knowledge bases
* Citation with exact page numbers
* Document preview
* Improved retrieval evaluation
* Deployment with a production-ready backend

---

# Learning Outcomes

This project demonstrates practical understanding of:

* Retrieval-Augmented Generation
* Large Language Models
* Embeddings
* Semantic Search
* Vector Databases
* PDF Processing
* Text Chunking
* FastAPI
* REST APIs
* Frontend and backend integration
* Environment Variables
* AI application development

---

# Assignment Requirements Checklist

| Requirement               | Status    |
| ------------------------- | --------- |
| 5 Python PDF chapters     | Completed |
| PDF text extraction       | Completed |
| Text chunking             | Completed |
| Embedding generation      | Completed |
| Local vector database     | Completed |
| ChromaDB                  | Completed |
| FastAPI application       | Completed |
| Groq LLM integration      | Completed |
| Retrieval pipeline        | Completed |
| AI-generated answers      | Completed |
| Web interface             | Completed |
| Source display            | Completed |
| `.env` API key protection | Completed |

---

# Screenshots for Submission

The following screenshots can be included in the assignment submission:

1. PyQuery home page
2. Five uploaded Python PDF chapters
3. PDF upload/process screen
4. Embedding generation in terminal
5. ChromaDB/vector database folder
6. Question and generated answer
7. Retrieved source information
8. Three different question-answer examples
9. Deployed application

---

# GitHub

Repository:

```text
https://github.com/YOUR_USERNAME/PyQuery
```

Replace the URL above with the actual GitHub repository URL after creating the repository.

---

# Author

**Haziqa Shakir Khan**

AI & Data Science Student
Python | Machine Learning | Deep Learning | RAG | Generative AI

GitHub:

```text
https://github.com/haziqashakirkhan
```

LinkedIn:

```text
https://www.linkedin.com/in/haziqa-shakir-khan-8923513a6/
```

---

# Conclusion

PyQuery demonstrates how Retrieval-Augmented Generation can be used to build a document-based AI study assistant.

The application combines:

```text
PDF Processing
      +
Text Chunking
      +
Embeddings
      +
ChromaDB
      +
Semantic Retrieval
      +
Groq LLM
      +
FastAPI
      =
AI Study Assistant
```

The project provides a practical implementation of a complete RAG pipeline where students can ask questions and receive answers grounded in their Python study material.

```
```
