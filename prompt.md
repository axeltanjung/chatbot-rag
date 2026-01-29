# 🎧 Vibe Coding Prompt: Full-Stack Chatbot (LLM + RAG + Vector DB + UI)

## Role & Mindset

You are a **senior AI engineer + product-minded full-stack developer**.
You build **production-grade AI systems**, not demos.

Principles:

* Explainability > magic
* Modular > monolithic
* Latency-aware, cost-aware
* Clear trade-offs and assumptions

The goal is to build a **chatbot with memory and knowledge grounding (RAG)**, wrapped in a **clean, modern UI**.

---

## 🎯 Product Goal

Build a chatbot application that:

1. Uses an LLM for conversational intelligence
2. Uses **RAG (Retrieval-Augmented Generation)** to answer questions based on user-provided documents
3. Stores embeddings in a **vector database**
4. Has a **clean, minimal UI** suitable for demo *and* real usage
5. Is explainable: users can see *why* an answer was generated

Target users:

* Technical users (data, product, ops)
* Non-technical users uploading PDFs / docs

Non-goals:

* No over-engineering
* No fancy animations that hurt usability

---

## 🧠 System Architecture (Must Follow)

### High-Level Flow

1. User uploads documents (PDF, DOCX, TXT)
2. Backend:

   * Extracts text
   * Chunks content
   * Generates embeddings
   * Stores embeddings in vector DB
3. User asks a question
4. Backend:

   * Converts question → embedding
   * Retrieves top-k relevant chunks
   * Injects them into LLM prompt (RAG)
5. LLM generates grounded answer
6. UI displays:

   * Final answer
   * Retrieved sources (collapsible)

---

## 🧱 Tech Stack (Opinionated but Adjustable)

### Backend

* Python
* FastAPI
* LangChain **or** LlamaIndex (justify choice)
* OpenAI / Anthropic / local LLM via API abstraction

### Vector Database (Pick ONE and justify)

* FAISS (local, simple)
* ChromaDB
* Pinecone (managed)

### Frontend

* React (or Next.js if SSR is useful)
* TailwindCSS
* shadcn/ui

### Embeddings

* OpenAI `text-embedding-3-large` **or equivalent**
* Explicitly state embedding dimension and implications

---

## 📦 Backend Requirements

### 1. Document Ingestion Pipeline

Must include:

* File type validation
* Text extraction per format
* Chunking strategy:

  * chunk_size
  * overlap
  * rationale (semantic vs fixed)

Output:

```json
{
  "chunk_id": "uuid",
  "text": "...",
  "metadata": {
    "source": "filename.pdf",
    "page": 3
  }
}
```

---

### 2. Vector Store Layer

Requirements:

* Upsert embeddings
* Similarity search (cosine or dot, justify)
* Configurable top-k
* Metadata filtering support

Explicitly expose:

* Index name
* Embedding dimension
* Persistence strategy

---

### 3. RAG Prompt Design

Design a **strict prompt** that:

* Forces grounding to retrieved context
* Refuses to hallucinate
* Cites sources

Example behavior rules:

* If context is insufficient → say "I don’t know"
* Never use outside knowledge unless explicitly allowed

---

### 4. Chat Endpoint

API Contract:

```json
POST /chat
{
  "query": "string",
  "chat_history": [...],
  "top_k": 5
}
```

Response:

```json
{
  "answer": "string",
  "sources": [...],
  "confidence": 0.0
}
```

Explain how confidence is approximated (heuristic, similarity score, etc).

---

## 🎨 Frontend / UI Requirements

### Layout

* Left sidebar:

  * Document upload
  * List of indexed documents
* Main panel:

  * Chat interface

---

### Chat UI

Features:

* Chat bubbles (user vs assistant)
* Loading state (streaming preferred)
* Error states
* Source toggle per answer

Visual vibe:

* Clean
* Minimal
* Developer-tool aesthetic

---

### UX Must-Haves

* Disable send when no documents indexed (optional toggle)
* Show which documents were used
* Clear chat history

---

## 🔍 Explainability Layer (Critical)

For each answer, expose:

* Retrieved chunks
* Similarity scores
* Prompt sent to LLM (redacted if needed)

This can be:

* Developer mode toggle
* Accordion UI

---

## ⚖️ Trade-offs to Explicitly Address

You must clearly explain:

* Why this vector DB
* Chunk size trade-offs
* Latency vs accuracy
* Cost control strategies
* Failure modes (empty retrieval, bad OCR, long context)

---

## 🧪 Testing & Validation

Include:

* Unit test for chunking
* Smoke test for retrieval quality
* Manual test checklist

---

## 🚀 Stretch Goals (Optional)

* Conversation memory summarization
* Hybrid search (BM25 + vector)
* Multi-collection support
* Role-based system prompts

---

## 🧠 Final Instruction

Build this as if:

* It will be reviewed by a senior AI engineer
* It may be deployed tomorrow

Clarity, robustness, and reasoning matter more than clever tricks.
