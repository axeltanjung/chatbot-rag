# 🆓 Using Free Models with OpenRouter

## What Changed?

The application now uses **OpenRouter** instead of OpenAI, giving you access to **completely free models** with no API key required!

---

## ✨ Free Models Available

### LLM Models (for chat responses):
1. **`google/gemma-2-9b-it:free`** ⭐ (Recommended)
   - Google's Gemma 2 model
   - 9B parameters
   - Good quality responses

2. **`meta-llama/llama-3.1-8b-instruct:free`**
   - Meta's Llama 3.1
   - 8B parameters
   - Strong performance

3. **`mistralai/mistral-7b-instruct:free`**
   - Mistral 7B
   - Fast and efficient

### Embedding Models (for document search):
1. **`thenlper/gte-large:free`** ⭐ (Recommended)
   - 1024 dimensions
   - Good quality embeddings

2. **`nomic-ai/nomic-embed-text-v1.5:free`**
   - 768 dimensions
   - Faster, smaller

---

## 🚀 Quick Start (No API Key Needed!)

### 1. The `.env` file is already configured!

It's set to use the free tier:
```env
OPENROUTER_API_KEY=sk-or-v1-free
LLM_MODEL=google/gemma-2-9b-it:free
EMBEDDING_MODEL=thenlper/gte-large:free
```

### 2. Just run the application!

**Backend:**
```bash
cd backend
venv\Scripts\activate
python main.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

That's it! No API key signup required! 🎉

---

## 🔧 Switching Models

Want to try a different model? Just edit `.env`:

```env
# Try Llama instead of Gemma
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Or try Mistral
LLM_MODEL=mistralai/mistral-7b-instruct:free
```

Restart the backend and you're good to go!

---

## 📊 Free Tier Limits

OpenRouter's free tier has some limits:
- **Rate limits**: ~20 requests/minute per model
- **No credit card required**
- **No signup required** for basic usage

For higher limits, you can:
1. Sign up at https://openrouter.ai
2. Get a free API key
3. Replace `sk-or-v1-free` with your key

---

## 🆚 OpenAI vs OpenRouter Free Models

| Feature | OpenAI (Paid) | OpenRouter (Free) |
|---------|---------------|-------------------|
| **Cost** | $0.01-0.03 per 1K tokens | **FREE** |
| **API Key** | Required (credit card) | **Not required** |
| **Quality** | GPT-4 (best) | Gemma/Llama (very good) |
| **Speed** | Fast | Fast |
| **Rate Limits** | High | Moderate |

---

## 💡 Tips for Best Results

### For Better Quality:
- Use `google/gemma-2-9b-it:free` (current default)
- Increase `TOP_K` to 7 in `.env`
- Lower `TEMPERATURE` to 0.5

### For Faster Responses:
- Use `mistralai/mistral-7b-instruct:free`
- Use `nomic-ai/nomic-embed-text-v1.5:free` for embeddings
- Reduce `MAX_TOKENS` to 500

---

## 🔍 How It Works

The code now uses OpenRouter's API which is compatible with OpenAI's format:

```python
# Before (OpenAI):
client = openai.OpenAI(api_key="sk-...")

# After (OpenRouter):
client = openai.OpenAI(
    api_key="sk-or-v1-free",
    base_url="https://openrouter.ai/api/v1"
)
```

Same code, different endpoint, **completely free**! 🎉

---

## 🚨 Troubleshooting

### "Rate limit exceeded"
- Wait a minute and try again
- Free tier has ~20 requests/minute
- Consider getting a free OpenRouter account for higher limits

### "Model not found"
- Check model name in `.env`
- Make sure it ends with `:free`
- See available models at: https://openrouter.ai/models?order=newest&supported_parameters=tools&max_price=0

### "Connection error"
- Check internet connection
- OpenRouter API might be temporarily down
- Try again in a few minutes

---

## 📚 More Free Models

Want to explore more free models? Visit:
https://openrouter.ai/models?max_price=0

Filter by:
- **Price**: $0.00 (free)
- **Type**: Chat or Embedding
- **Context**: How much text it can handle

---

## ✅ What You Get for FREE

✅ Unlimited document uploads  
✅ Unlimited questions  
✅ Source citations  
✅ Confidence scores  
✅ Developer mode  
✅ All features working  
✅ No credit card needed  
✅ No signup required (basic tier)  

---

**Enjoy your free RAG chatbot!** 🚀
