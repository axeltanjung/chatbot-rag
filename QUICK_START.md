# Quick Reference Guide

## 🚀 Quick Start

### 1. Setup (First Time Only)

```bash
# Run setup script
setup.bat

# OR manually:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd ..\frontend
npm install
```

### 2. Configure API Key

Edit `.env` file:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Start Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
chatbot-rag/
├── backend/                 # FastAPI backend
│   ├── main.py             # App entry point
│   ├── config.py           # Settings
│   ├── models.py           # Data models
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── rag_engine.py
│   ├── prompts.py
│   ├── routes/
│   │   ├── documents.py    # Document endpoints
│   │   └── chat.py         # Chat endpoint
│   └── tests/
│       ├── test_chunking.py
│       └── test_retrieval.py
├── frontend/               # React frontend
│   └── src/
│       ├── components/
│       │   ├── Sidebar.jsx
│       │   ├── ChatPanel.jsx
│       │   ├── Message.jsx
│       │   └── SourceCard.jsx
│       ├── services/
│       │   └── api.js
│       └── App.jsx
└── .env                    # Configuration
```

---

## 🔧 Configuration Options

### `.env` File

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | **Required** OpenAI API key |
| `LLM_MODEL` | gpt-4 | LLM model to use |
| `EMBEDDING_MODEL` | text-embedding-3-small | Embedding model |
| `CHUNK_SIZE` | 1000 | Characters per chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `TOP_K` | 5 | Number of chunks to retrieve |
| `TEMPERATURE` | 0.7 | LLM temperature |

---

## 📝 Common Tasks

### Upload a Document

1. Click upload area or drag-and-drop
2. Select PDF, DOCX, or TXT file
3. Wait for processing (shows in sidebar)

### Ask a Question

1. Type question in input field
2. Press Enter or click Send
3. View answer with sources

### View Sources

1. Click "X sources" link below answer
2. See similarity scores and previews
3. Click again to collapse

### Enable Developer Mode

1. Toggle "Developer Mode" in sidebar
2. View prompts sent to LLM
3. See debug information

### Delete a Document

1. Hover over document in sidebar
2. Click trash icon
3. Confirm deletion

---

## 🧪 Testing

### Run Unit Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### Manual Test Checklist

- [ ] Upload PDF
- [ ] Upload DOCX  
- [ ] Upload TXT
- [ ] Ask relevant question
- [ ] Verify citations
- [ ] Test out-of-scope question
- [ ] Check confidence scores
- [ ] View sources
- [ ] Enable developer mode
- [ ] Delete document
- [ ] Clear chat

---

## 🐛 Troubleshooting

### Backend Issues

**Error: "OPENAI_API_KEY not set"**
- Edit `.env` file and add your API key

**Error: "Module not found"**
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

**Port 8000 already in use**
- Change `API_PORT` in `.env`
- Or kill process: `netstat -ano | findstr :8000`

### Frontend Issues

**Error: "Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check `vite.config.js` proxy settings

**Blank page**
- Check browser console for errors
- Verify Node version: `node --version` (need 18+)

**Upload fails**
- Check file type (PDF, DOCX, TXT only)
- Verify backend is running
- Check backend logs

---

## 🎯 API Endpoints

### Documents

```http
POST /api/documents/upload
GET  /api/documents/
DELETE /api/documents/{filename}
GET  /api/documents/info
```

### Chat

```http
POST /api/chat/
GET  /api/chat/health
```

### Example Chat Request

```json
POST /api/chat/
{
  "query": "What is the main topic?",
  "chat_history": [],
  "top_k": 5
}
```

### Example Response

```json
{
  "answer": "Based on the documents...",
  "sources": [
    {
      "chunk_id": "uuid",
      "text": "...",
      "source": "document.pdf",
      "page": 3,
      "similarity_score": 0.92
    }
  ],
  "confidence": 0.87
}
```

---

## 🔒 Security Notes

- Never commit `.env` file
- Keep API keys secret
- Use environment variables in production
- Enable CORS only for trusted origins

---

## 📊 Performance Tips

### Optimize Chunking

- Smaller chunks = more precise, but may lose context
- Larger chunks = more context, but less precise
- Adjust `CHUNK_SIZE` in `.env`

### Reduce Costs

- Use `text-embedding-3-small` instead of `large`
- Lower `MAX_TOKENS` for shorter responses
- Reduce `TOP_K` to retrieve fewer chunks

### Improve Accuracy

- Use `text-embedding-3-large` (slower, more expensive)
- Increase `TOP_K` for more context
- Adjust `TEMPERATURE` (lower = more consistent)

---

## 🚢 Deployment

### Docker

```bash
docker-compose up -d
```

### Manual Deployment

1. Set production environment variables
2. Build frontend: `npm run build`
3. Serve with production server (gunicorn, nginx)
4. Use managed vector DB (Pinecone) for scale

---

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [React Docs](https://react.dev/)
