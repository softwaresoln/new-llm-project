from flask import Flask, request, jsonify, render_template
import os
import shutil
import atexit
import logging
import re
import requests
from dotenv import load_dotenv

# ----------------------------
# Modern LangChain Imports
# ----------------------------
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")
OPENROUTER_PROVIDER = os.getenv("OPENROUTER_PROVIDER", "").strip()
SAMPLE_FILE = os.getenv("SAMPLE_FILE", "sample2.txt")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# ----------------------------
# Flask + Logging
# ----------------------------
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fintax")

vectorstore = None
retriever = None

# ----------------------------
# Cleanup on exit
# ----------------------------
def cleanup_chroma_db():
    global vectorstore, retriever
    try:
        vectorstore = None
        retriever = None
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH, ignore_errors=True)
            logger.info("Removed Chroma DB directory on exit.")
    except Exception as e:
        logger.exception("Error during cleanup_chroma_db: %s", e)

atexit.register(cleanup_chroma_db)

# ----------------------------
# Initialize Chroma DB
# ----------------------------
def initialize_chroma_db(persist_directory=CHROMA_DB_PATH, sample_file=SAMPLE_FILE, chunk_size=500):
    global vectorstore, retriever

    # Clean existing DB
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory, ignore_errors=True)
        logger.info("Removed existing persist directory for clean start.")

    # Load text
    if not os.path.exists(sample_file):
        logger.warning("%s not found — vectorstore will be empty.", sample_file)
        text = ""
    else:
        with open(sample_file, "r", encoding="utf-8") as f:
            text = f.read()

    if not text.strip():
        logger.error("No content found in %s", sample_file)
        return None

    # Split into sections using regex
    sections = re.split(r"(Section\s+\d+[\.:])", text)
    chunks, metadatas = [], []

    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            section_title = sections[i].strip()
            section_text = sections[i + 1] if i + 1 < len(sections) else ""
            full_text = f"{section_title} {section_text}".strip()

            # Break into 500-character chunks
            for j in range(0, len(full_text), chunk_size):
                chunk = full_text[j:j + chunk_size]
                chunks.append(chunk)
                metadatas.append({
                    "source": os.path.basename(sample_file),
                    "section": section_title,
                    "chunk_index": j // chunk_size
                })
    else:
        # fallback
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
            metadatas.append({
                "source": os.path.basename(sample_file),
                "section": "Unknown",
                "chunk_index": i // chunk_size
            })

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        metadatas=metadatas
    )
    # Note: persist() is no longer needed in Chroma 0.4.x as it auto-persists
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    logger.info(f"✅ Indexed {len(chunks)} chunks with section metadata.")
    return vectorstore

# ----------------------------
# Initialize DB
# ----------------------------
try:
    vectorstore = initialize_chroma_db()
    logger.info("Chroma DB initialized successfully.")
except Exception as e:
    logger.exception("Error initializing Chroma DB: %s", e)
    try:
        CHROMA_DB_PATH = "./chroma_db_backup"
        vectorstore = initialize_chroma_db(persist_directory=CHROMA_DB_PATH)
        logger.info("Chroma DB initialized using backup directory.")
    except Exception as e2:
        logger.exception("Failed to initialize Chroma DB (backup): %s", e2)
        raise

if vectorstore and retriever is None:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ----------------------------
# Prompt Template
# ----------------------------
PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant named TaxAJ. Use the following GST context to answer the question.
If the context does not contain the answer, answer based on your general tax knowledge.

Context:
{context}

Question:
{question}

Answer:
"""
)

# ----------------------------
# OpenRouter API Helper
# ----------------------------
def call_openrouter_chat(prompt_text, model=OPENROUTER_MODEL, provider_name=OPENROUTER_PROVIDER):
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set.")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt_text}]
    }

    if provider_name:
        payload["provider"] = {"name": provider_name}

    resp = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
    if not resp.ok:
        raise RuntimeError(f"OpenRouter returned {resp.status_code}: {resp.text}")
    return resp.json()

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        return "Tax service - use /chat or /query endpoints."

@app.route("/query", methods=["POST"])
def query():
    global retriever, vectorstore
    try:
        if retriever is None:
            return jsonify({"error": "Retriever not initialized"}), 500

        data = request.get_json(force=True)
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "question is required"}), 400

        results = []
        if hasattr(vectorstore, "similarity_search_with_score"):
            docs_scores = vectorstore.similarity_search_with_score(question, k=3)
            for doc, score in docs_scores:
                meta = getattr(doc, "metadata", {})
                results.append({
                    "content": doc.page_content.strip(),
                    "source": meta.get("source", "unknown"),
                    "section": meta.get("section", "unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "score": round(float(score), 4) if score else None
                })
        else:
            docs = retriever.invoke(question)
            for doc in docs:
                meta = getattr(doc, "metadata", {})
                results.append({
                    "content": doc.page_content.strip(),
                    "source": meta.get("source", "unknown"),
                    "section": meta.get("section", "unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "score": None
                })

        # remove duplicates
        unique = []
        seen = set()
        for r in results:
            key = (r["section"], r["chunk_index"])
            if key not in seen:
                seen.add(key)
                unique.append(r)

        return jsonify({"question": question, "top_chunks": unique}), 200

    except Exception as e:
        logger.exception("Error in /query: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    global retriever
    try:
        if retriever is None:
            return jsonify({"error": "Retriever not initialized"}), 500

        data = request.get_json(force=True)
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "question is required"}), 400

        docs = retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in docs])
        prompt_text = PROMPT.format(context=context, question=question)

        data = call_openrouter_chat(prompt_text)
        reply = data["choices"][0]["message"]["content"]

        return jsonify({
            "question": question,
            "reply": reply,
            "sources": [getattr(doc, "metadata", {}) for doc in docs]
        })

    except Exception as e:
        logger.exception("Error in /chat: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    if vectorstore is None:
        return jsonify({"status": "error", "message": "Chroma DB not initialized"}), 500
    return jsonify({"status": "healthy", "message": "Service is running"})

# ----------------------------
# Run Flask
# ----------------------------
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", "5000"))
        app.run(debug=True, port=port)
    finally:
        cleanup_chroma_db()
