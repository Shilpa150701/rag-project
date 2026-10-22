
Local PDF RAG (Retrieval Augmented Generation)
A fully local RAG system that allows users to query PDF documents using natural language and receive context-aware answers with source references.

Features
Fully offline execution
Local LLM using Ollama
PDF document ingestion
Semantic search using FAISS
Embedding model: BAAI/bge-small-en-v1.5
Exact information retrieval from PDFs
Source file and page number tracking
Multiple PDF support
Extensible FastAPI backend
Architecture
PDF Documents
      |
      v
PyMuPDF Extraction
      |
      v
Text Chunking
      |
      +----------------+
      |                |
      v                v
     BM25          FAISS Vector DB
      |                |
      +-------+--------+
              |
              v
       Hybrid Retrieval
              |
              v
      Ollama (Qwen 2.5)
              |
              v
 Answer + Source + Page
Tech Stack
Backend
Python
LangChain
FAISS
PyMuPDF
Embeddings
BAAI/bge-small-en-v1.5
Local LLM
Ollama
Qwen2.5:1.5b
Search
Vector Search (FAISS)
BM25 Keyword Search
Project Structure
rag/
│
├── pdfs/
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
│
├── data/
│   ├── faiss_db/
│   └── chunks.pkl
│
├── build_index.py
├── ask.py
├── requirements.txt
├── README.md
└── .gitignore
Installation
Clone Repository
git clone https://github.com/<your-username>/local-pdf-rag.git

cd local-pdf-rag
Create Virtual Environment
python -m venv rag_venv
Activate Environment
Windows

rag_venv\Scripts\activate
Linux/Mac

source rag_venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Install Ollama
Download and install Ollama:

https://ollama.com/download

Pull the model:

ollama pull qwen2.5:1.5b
Verify:

ollama list
Start server:

ollama serve
Add PDFs
Place all PDF files inside:

pdfs/
Example:

pdfs/
├── salary_slip_jan.pdf
├── salary_slip_feb.pdf
├── policy.pdf
├── offer_letter.pdf
└── merit_letter.pdf
Build Index
Generate embeddings and create vector database.

python build_index.py
Output:

Pages Loaded: 250
Chunks Created: 500
Index Saved Successfully
Query Documents
Run:

python ask.py
Example:

Question:
What is the net salary for March 2025?
Response:

Net Salary: ₹85,450

Source:
salary_slip_mar_2025.pdf

Page:
1
Supported Queries
Examples:

What is my salary for March 2025?

What is my employee ID?

What does the leave policy say regarding maternity leave?

What is my joining date?

What is the bonus amount mentioned in the merit letter?

Summarize the offer letter.
Current Limitations
OCR-based scanned PDFs are not supported by default.
Large collections may require higher RAM.
Qwen 1.5B may provide less detailed reasoning than larger models.
Future Enhancements
Streamlit UI
FastAPI REST API
OCR for scanned PDFs
Citation-based answers
Multi-language support
Metadata filtering
Reranking
ChromaDB support
Docker deployment
Performance
Recommended System:

RAM: 8 GB+
CPU: Intel i5/Ryzen 5+
Storage: SSD
Minimum:

RAM: 4 GB
Example Workflow
1. Add PDFs
2. Run build_index.py
3. Ask questions using ask.py
4. Retrieve exact content from documents
5. View source file and page number
Author
Built as a local Retrieval Augmented Generation (RAG) solution using:

LangChain
FAISS
Ollama
Qwen2.5
PyMuPDF
