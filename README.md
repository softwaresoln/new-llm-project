🧾 Tax – AI-Powered Tax & GST Assistant

Tax is an intelligent, domain-specific chatbot built using Flask, LangChain, ChromaDB, and OpenRouter API.
It can answer tax and GST-related questions by retrieving relevant context from uploaded or sample knowledge bases (like sample2.txt).

🚀 Features

✅ Flask-based REST API for chatbot and retrieval
✅ Retrieval-Augmented Generation (RAG) using LangChain + Chroma
✅ SentenceTransformer embeddings (all-MiniLM-L6-v2)
✅ OpenRouter model integration (e.g., qwen/qwen3-4b:free)
✅ Metadata for sections, source, and chunk indices
✅ Auto cleanup of Chroma DB on exit
✅ Configurable .env parameters

 Project Structure
📁 TaxAJ-Chatbot
│
├── app.py                  # Flask backend (main logic)
├── sample2.txt             # Example GST knowledge base
├── templates/
│   └── index.html          # Optional homepage
├── chroma_db/              # Auto-generated vector database
├── .env                    # Environment configuration
├── requirements.txt        # Dependencies
└── README.md               # Documentation

⚙️ Environment Setup
1️⃣ Create a .env file
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=qwen/qwen3-4b:free
OPENROUTER_PROVIDER=
SAMPLE_FILE=sample2.txt
CHROMA_DB_PATH=./chroma_db
REQUEST_TIMEOUT=30
PORT=5000


🔑 Get your OpenRouter API key from https://openrouter.ai/keys

2️⃣ Install Dependencies
pip install -r requirements.txt


requirements.txt:

flask
langchain
chromadb
sentence-transformers
python-dotenv
requests

3️⃣ Run the Server
python app.py


Then open:
👉 http://localhost:5000

🌐 API Endpoints
🔍 POST /query

Retrieves relevant chunks from the knowledge base.

Request:

{ "question": "What is input tax credit under GST?" }


Response:

{
  "question": "What is input tax credit under GST?",
  "top_chunks": [
    {
      "content": "Section 16: Eligibility and conditions for taking input tax credit...",
      "source": "sample2.txt",
      "section": "Section 16",
      "chunk_index": 0,
      "score": 0.89
    }
  ]
}

💬 POST /chat

Generates a contextual answer using retrieved chunks.

Request:

{ "question": "Explain GST composition scheme." }


Response:

{
  "question": "Explain GST composition scheme.",
  "reply": "Under GST, the composition scheme allows small taxpayers...",
  "sources": [
    {
      "source": "sample2.txt",
      "section": "Section 10",
      "chunk_index": 1
    }
  ]
}

❤️ GET /health

Checks the service status.

Response:

{
  "status": "healthy",
  "message": "Service is running"
}

🧠 Visual Workflow Diagram (Markdown Summary)
flowchart TD
    A[📄 Sample File (sample2.txt)] --> B[🧩 Split Text into 500-char Chunks]
    B --> C[🔤 Generate Embeddings (SentenceTransformer)]
    C --> D[💾 Store in ChromaDB with Metadata]
    D --> E[🔍 Retriever: Find Top 3 Relevant Chunks]
    E --> F[🧠 Create Context with PromptTemplate]
    F --> G[🤖 OpenRouter API (Qwen/Qwen3-4B)]
    G --> H[💬 AI Reply Returned]
    

🧩 This diagram shows how text is embedded, stored, retrieved, and used to generate contextual AI responses.


🧹 Automatic Cleanup

When the app stops, it deletes the ChromaDB directory to prevent stale data:

atexit.register(cleanup_chroma_db)
