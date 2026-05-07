# 🚀 Quick Start Guide

Get the RAG chatbot running in 10 minutes!

## Option 1: Automatic Setup (Recommended for Windows)

```bash
# 1. Double-click setup.bat
# 2. The script will:
#    - Create virtual environment
#    - Install dependencies
#    - Set up .env file
#    - Initialize vector store from PDFs

# 3. EDIT .env and add your OPENAI_API_KEY:
#    Open .env in notepad and uncomment the line:
#    OPENAI_API_KEY=sk-your-actual-key-here

# 4. Verify setup worked:
python utils.py
```

Output should show your PDFs and configuration.

## Option 2: Manual Setup (All Platforms)

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment
```bash
# Copy template
cp .env.example .env

# Edit .env file - ADD YOUR OPENAI_API_KEY
# Option A: OpenAI (best quality)
#   Get key from: https://platform.openai.com/api-keys
#   OPENAI_API_KEY=sk-...

# Option B: Ollama (free, local)
#   Download: https://ollama.ai
#   Run: ollama pull mistral
#   Update main.py to use Ollama
```

### Step 4: Initialize Vector Store
```bash
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

Wait for completion (~5 minutes). Creates `chroma_db/` folder with embeddings.

### Step 5: Start Backend
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Start Frontend (New Terminal)
```bash
# Activate venv in new terminal first
streamlit run app.py
```

Opens http://localhost:8501 automatically

## Testing

### Via Streamlit UI
1. Open http://localhost:8501
2. Ask: "What is the leave policy?"
3. Should see answer + sources

### Via API
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the leave policy?"}'
```

## troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Reinstall: `pip install -r requirements.txt` |
| `OPENAI_API_KEY not found` | Edit `.env` and add your key, restart `main.py` |
| `Cannot connect to API` | Check: Is `main.py` running? Is it on port 8000? |
| `Vector store not found` | Run: `python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"` |
| `Slow responses` | Use `gpt-3.5-turbo` instead of `gpt-4` in .env |

## Next Steps

✅ Try these sample questions:
- "How many days of leave do I get?"
- "What is the WFH policy?"
- "What is the notice period for resignation?"
- "What password policy do we have?"
- "Does SWS AI provide health insurance?"

📚 Full documentation: See README.md

💡 For production deployment: See "Deployment" section in README.md

---

**That's it!** You have a working RAG chatbot.
