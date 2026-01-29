# RAG Chatbot

A production-grade chatbot with Retrieval-Augmented Generation (RAG), vector database, and modern UI.

**✨ Now using FREE models - No API key or credit card required!**

## Features

- 🤖 **Conversational AI** - Powered by Google Gemma 2 (FREE)
- 📚 **Document Grounding** - RAG ensures answers are based on your documents
- 🔍 **Source Citations** - Every answer includes source references
- 💾 **Vector Database** - ChromaDB for efficient similarity search
- 🎨 **Modern UI** - Clean, dark-mode interface with React + TailwindCSS
- 🔬 **Explainability** - See retrieved chunks, similarity scores, and prompts
- 📊 **Confidence Scores** - Understand answer reliability
- 🆓 **Completely FREE** - Uses OpenRouter's free tier

## Architecture

### Backend (FastAPI + Python)
- **Document Processing**: PDF, DOCX, TXT extraction and chunking
- **Embeddings**: Free embedding model via OpenRouter
- **Vector Store**: ChromaDB with cosine similarity
- **RAG Engine**: Retrieval + prompt construction + LLM generation
- **LLM**: Google Gemma 2 or Meta Llama 3.1 (FREE)

### Frontend (React + Vite)
- **Document Management**: Upload, list, delete documents
- **Chat Interface**: Real-time chat with loading states
- **Source Display**: Collapsible source citations
- **Developer Mode**: View prompts and debug information

## Prerequisites

- Python 3.9+
- Node.js 18+
- **No API key needed!** (Uses free OpenRouter models)

## Installation

### 1. Clone Repository

```bash
cd d:\project\chatbot-rag
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Environment Configuration

The `.env` file is already configured with FREE models!

```bash
# Already set to use free models - no changes needed!
OPENROUTER_API_KEY=sk-or-v1-free
LLM_MODEL=google/gemma-2-9b-it:free
EMBEDDING_MODEL=thenlper/gte-large:free
```

**No API key signup required!** Just run the app.

Want to use different free models? See `FREE_MODELS_GUIDE.md`

## Running the Application

### Start Backend

```bash
cd backend
python main.py
```

Backend will run on `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## Usage

1. **Upload Documents**
   - Click upload area or drag-and-drop PDF/DOCX/TXT files
   - Documents are automatically processed and indexed

2. **Ask Questions**
   - Type questions in the chat input
   - Receive grounded answers with source citations

3. **View Sources**
   - Click on source count to expand citations
   - See similarity scores and chunk previews

4. **Developer Mode**
   - Toggle in sidebar to see prompts and debug info

## Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Manual Testing Checklist

- [ ] Upload PDF document
- [ ] Upload DOCX document
- [ ] Upload TXT document
- [ ] Ask question about uploaded content
- [ ] Verify answer includes citations
- [ ] Test "I don't know" response for out-of-scope query
- [ ] Check confidence scores
- [ ] Expand source citations
- [ ] Enable developer mode and view prompt
- [ ] Delete document
- [ ] Clear chat history

## Configuration

### `.env` File

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | sk-or-v1-free | Free tier key (no signup needed) |
| `LLM_MODEL` | google/gemma-2-9b-it:free | Free LLM model |
| `EMBEDDING_MODEL` | thenlper/gte-large:free | Free embedding model |
| `CHUNK_SIZE` | 1000 | Characters per chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `TOP_K` | 5 | Number of chunks to retrieve |
| `TEMPERATURE` | 0.7 | LLM temperature |

### Available Free Models

**LLM Models:**
- `google/gemma-2-9b-it:free` (Recommended)
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

**Embedding Models:**
- `thenlper/gte-large:free` (Recommended, 1024 dims)
- `nomic-ai/nomic-embed-text-v1.5:free` (768 dims)

See `FREE_MODELS_GUIDE.md` for more details.

## Architecture Decisions

### Latency vs Accuracy

- Using smaller embedding model for speed
- Top-k=5 balances context vs noise
- No streaming (simpler implementation)

### Cost Control

- Batch embedding generation
- Smaller embedding model
- Configurable max tokens

### Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty retrieval | Return "No documents indexed" message |
| Bad OCR | Validate text length, warn user |
| Long context | Truncate to model's context window |
| API failures | Retry with exponential backoff |

## API Documentation

### Upload Document

```http
POST /api/documents/upload
Content-Type: multipart/form-data

file: <file>
```

### List Documents

```http
GET /api/documents/
```

### Chat

```http
POST /api/chat/
Content-Type: application/json

{
  "query": "What is the main topic?",
  "chat_history": [],
  "top_k": 5
}
```

## Project Structure

```
chatbot-rag/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── rag_engine.py
│   ├── prompts.py
│   ├── routes/
│   │   ├── documents.py
│   │   └── chat.py
│   ├── tests/
│   │   ├── test_chunking.py
│   │   └── test_retrieval.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ChatPanel.jsx
│   │   │   ├── Message.jsx
│   │   │   └── SourceCard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── REQUIREMENTS.md
└── README.md
```

## Troubleshooting

### Backend won't start

- Check Python version: `python --version` (need 3.9+)
- Verify virtual environment is activated
- Check `.env` file exists (should already be configured)

### "Rate limit exceeded"

- OpenRouter free tier has ~20 requests/minute
- Wait a minute and try again
- Consider getting a free OpenRouter account for higher limits at https://openrouter.ai

### Frontend won't start

- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and run `npm install` again
- Check backend is running on port 8000

### Upload fails

- Verify file type is PDF, DOCX, or TXT
- Check file is not corrupted
- Ensure `pypdf` and `python-docx` are installed

### No answers returned

- Verify documents are uploaded and indexed
- Check internet connection (OpenRouter API needs internet)
- Look at backend logs for errors
- Try a different free model in `.env`

## License

MIT

## Contributing

Contributions welcome! Please follow the existing code style and add tests for new features.
