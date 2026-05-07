# 🎯 START HERE - Getting Your Chatbot Running

## ⚡ Super Quick Start (10 Minutes)

### Step 1️⃣ Windows Users Only
```batch
double-click setup.bat
```
Or manually:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2️⃣ All Users - Add Your API Key
```bash
# Edit .env file with any text editor
# OR copy and edit:
cp .env.example .env

# Add this line to .env:
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Get free key: https://platform.openai.com/api-keys
```

### Step 3️⃣ Initialize (One-Time, ~5 min)
```bash
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

### Step 4️⃣ Terminal 1 - Start Backend
```bash
python main.py
```

**See:** `INFO: Uvicorn running on http://0.0.0.0:8000`

### Step 5️⃣ Terminal 2 - Start Frontend
```bash
streamlit run app.py
```

**Browser opens automatically to http://localhost:8501**

### Step 6️⃣ Ask Questions! 🎉

Example questions:
- "What is the leave policy?"
- "How many days of sick leave?"
- "What's the WFH policy?"
- "Does SWS offer health insurance?"

---

## 📊 What You Have

```
Project Ready! ✅

Backend:  FastAPI + LangChain + ChromaDB
          → http://localhost:8000

Frontend: Streamlit
          → http://localhost:8501

Docs:     FastAPI interactive docs
          → http://localhost:8000/docs

PDFs:     10 company documents processed
          → 10 MB → Chunked → Embedded → Indexed

Embeddings: SentenceTransformers (local, fast)

LLM:      OpenAI GPT-3.5-turbo (your choice of model)

Vector DB: ChromaDB (persistent, local)
```

---

## 🧪 Verify It Works

```bash
# Test the system
python test_system.py

# Should show all ✅ checks passing
```

---

## 🔑 Critical: Add Your OpenAI API Key!

❌ **DON'T SKIP THIS** - The entire system depends on it

### How to Get API Key (Free $5 credit)

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Edit `.env` file
5. Add: `OPENAI_API_KEY=sk-...`

### Alternative: Use Ollama (Free, Local)

Download from https://ollama.ai

```bash
ollama pull mistral
```

Then modify `main.py` to use Ollama instead of OpenAI.

---

## 📁 Project Layout

```
Your Chatbot Folder:
├── 📄 PDFs (10 files)
│   └── SWS-AI-*.pdf
│
├── 🔧 Core Files
│   ├── main.py           ← Run this for backend
│   ├── app.py            ← Run this for frontend
│   ├── document_ingestion.py
│   └── rag_system.py
│
├── ⚙️  Configuration
│   ├── .env              ← ADD YOUR API KEY HERE
│   ├── config.py
│   └── requirements.txt
│
├── 📚 Documentation
│   ├── README.md
│   ├── QUICK_START.md
│   ├── COMPLETE_GUIDE.md
│   └── PROJECT_SUMMARY.md
│
└── 🚀 Auto-Generated
    └── chroma_db/        ← Created after step 3
```

---

## 🚀 The 3 Commands You Need

```bash
# Terminal 1: Initialize (ONE-TIME)
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"

# Terminal 2: Start Backend
python main.py

# Terminal 3: Start Frontend
streamlit run app.py
```

Then visit: http://localhost:8501

---

## ❓ Common Issues

| Issue | Fix |
|-------|-----|
| "Module not found" | `pip install -r requirements.txt` |
| "API key not found" | Edit `.env`, add your key |
| "Can't connect to API" | Check if `main.py` is running |
| "Vector store not found" | Run initialization command (Step 3) |

---

## 📞 Quick Help

Run this to check everything:
```bash
python test_system.py
```

Check API is running:
```bash
curl http://localhost:8000/health
```

---

## 🎯 Your Success Path

```
1. Get OpenAI Key
   ↓
2. pip install -r requirements.txt
   ↓
3. python -c "from document_ingestion import ..."
   ↓
4. python main.py
   ↓
5. streamlit run app.py
   ↓
6. http://localhost:8501
   ↓
7. Ask questions! 🎉
```

---

## 📖 Need More Help?

- **Fast guide:** QUICK_START.md
- **Complete reference:** COMPLETE_GUIDE.md
- **Full docs:** README.md
- **Overview:** PROJECT_SUMMARY.md

---

## ✨ All Done!

You have a **production-ready RAG chatbot** with:

✅ 10 company PDF documents indexed
✅ Semantic search powered by AI embeddings
✅ LLM-generated answers with sources
✅ Professional REST API
✅ Beautiful web UI
✅ Ready to deploy

**Time to first question: ~15 minutes**

**Let's go! 🚀**
