# 📚 Complete Setup & Usage Guide

## What Was Built

A production-ready **RAG (Retrieval Augmented Generation) Chatbot** that answers employee questions about company policies using AI. The system processes 10 company PDF documents and provides accurate, sourced answers.

### Project Contents

```
Company_Assistant_Chatbot/
├── 📄 Backend & Core
│   ├── main.py                          # FastAPI server ⚡
│   ├── document_ingestion.py            # PDF → Embeddings pipeline 📄
│   ├── rag_system.py                    # LLM + Retrieval logic 🧠
│   └── utils.py                         # Helper utilities 🛠️
│
├── 🎨 Frontend
│   └── app.py                           # Streamlit UI 🖥️
│
├── ⚙️  Configuration
│   ├── .env.example                     # Environment template
│   ├── config.py                        # Advanced settings
│   └── requirements.txt                 # Python dependencies
│
├── 📚 Documentation
│   ├── README.md                        # Full documentation (30+ sections)
│   ├── QUICK_START.md                   # Fast setup guide
│   └── This file
│
├── 🔧 Setup Scripts
│   ├── setup.bat                        # Windows setup (automatic)
│   ├── setup.sh                         # macOS/Linux setup
│   └── test_system.py                   # System diagnostics
│
├── 📑 Company Documents (10 PDFs)
│   ├── SWS-AI-company-overview.pdf
│   ├── SWS-AI-hr-policy.pdf
│   ├── SWS-AI-leave-policy.pdf
│   ├── SWS-AI-resignation-policy.pdf
│   ├── SWS-AI-wfh-policy.pdf
│   ├── SWS-AI-code-of-conduct.pdf
│   ├── SWS-AI-it-security-policy.pdf
│   ├── SWS-AI-performance-review.pdf
│   ├── SWS-AI-benefits-compensation.pdf
│   └── SWS-AI-onboarding-guide.pdf
│
└── 🔍 Auto-Generated (on first run)
    └── chroma_db/                       # Vector store with embeddings
```

---

## 🚀 Quick Start (5 Minutes)

### For Windows Users

```bash
# 1. Double-click: setup.bat
# 2. Wait for setup to complete
# 3. Edit .env file and add your OpenAI API key
# 4. Done! Follow next section
```

### For macOS/Linux Users

```bash
# 1. Run setup
bash setup.sh

# 2. Edit .env and add your API key
vi .env
```

### For All Users (Manual)

```bash
# 1. Create environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup configuration
cp .env.example .env
# Edit .env and add OPENAI_API_KEY=sk-...

# 4. Initialize vector store (ONE-TIME, ~5 minutes)
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

---

## 🎯 Running the Application

### Terminal 1: Start Backend API

```bash
# Make sure venv is activated
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**API is now ready at:**
- 📖 http://localhost:8000/docs (Interactive API docs)
- 🏥 http://localhost:8000/health (Health check)

### Terminal 2: Start Frontend UI

```bash
# In a NEW terminal, activate venv again
streamlit run app.py
```

**Browser opens automatically:**
- 💬 http://localhost:8501 (Chat interface)

### Now You're Ready!

Go to http://localhost:8501 and ask questions like:
- "What is the leave policy?"
- "How many days of sick leave?"
- "What's the WFH policy?"
- "Does SWS provide health insurance?"

---

## 🔑 Setup Configuration

### Step 1: Get OpenAI API Key

**Option A: OpenAI (Best Quality)**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key

**Option B: Use Ollama (Free, Local)**
1. Download Ollama: https://ollama.ai
2. Run: `ollama pull mistral`
3. It runs locally on `http://localhost:11434`

### Step 2: Configure the Project

Edit `.env` file:

```bash
# Option A: With OpenAI
OPENAI_API_KEY=sk-your-actual-key-here
LLM_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7

# Option B: With Ollama (modify main.py to use Ollama instead)
# LLM_MODEL=ollama
# OLLAMA_BASE_URL=http://localhost:11434
```

### Step 3: Test Configuration

```bash
python test_system.py
```

Should show:
```
✅ Python 3.8+ OK
✅ All 10 PDF files found
✅ All required project files present
✅ .env file configured with API key
✅ All dependencies installed
✅ Vector store exists
```

---

## 📊 How It Works

### The RAG Pipeline

```
User Question
    ↓
[Embedding] Convert to vector
    ↓
[Search] Find top-3 similar chunks in ChromaDB
    ↓
[Context] "Here are relevant excerpts from policies..."
    ↓
[LLM] "Based on this context, the answer is..."
    ↓
[Answer] Grounded response with source documents
```

### Example Interaction

**User:** "How many days of sick leave do I get?"

**System Process:**
1. Embeds question with SentenceTransformers
2. Searches ChromaDB for similar chunks
3. Retrieves: "Employees get 10 days of paid sick leave per year"
4. Adds to LLM prompt with document source
5. LLM generates: "According to HR Policy, you get 10 days of paid sick leave per calendar year..."
6. Shows source: "SWS-AI-hr-policy.pdf, Page 3"

---

## 💡 API Usage Examples

### Simple Query

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the leave policy?"}'
```

### Response Format

```json
{
  "answer": "According to the Leave Policy document, employees are entitled to 20 days of annual leave...",
  "sources": [
    {
      "source": "SWS-AI-leave-policy.pdf",
      "page": 1,
      "content": "Annual Leave: 20 days per calendar year, can be carried over..."
    }
  ]
}
```

### All API Endpoints

```
GET  /              # Welcome message
GET  /health        # Health check
GET  /docs          # API documentation
GET  /documents     # Document statistics
POST /chat          # Ask a question
```

---

## 🧪 Verification Checklist

✅ All files copied correctly? Check:
```bash
ls -la  # or dir on Windows
```

✅ PDFs loaded? Test:
```bash
python -c "from document_ingestion import DocumentIngestionPipeline; p = DocumentIngestionPipeline(); docs = p.load_all_pdfs(); print(f'Loaded {len(docs)} documents')"
```

✅ API working? Test:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","message":"All systems operational"}
```

✅ Frontend connected? Open:
```
http://localhost:8501
```

---

## 🔧 Troubleshooting

### "OPENAI_API_KEY not set"
```bash
# Check .env file
cat .env  # or type .env on Windows

# Should contain:
# OPENAI_API_KEY=sk-...

# If missing, edit the file and add it
```

### "ModuleNotFoundError: No module named 'langchain'"
```bash
pip install -r requirements.txt --upgrade
```

### "Cannot connect to API at http://localhost:8000"
```bash
# Check if main.py is running in another terminal
# Check if port 8000 is in use:
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000
```

### "Vector store not found"
```bash
# Initialize it:
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

### "Streamlit running locally but can't connect"
```bash
# Check port 8501 is accessible
# Try: http://0.0.0.0:8501 or http://127.0.0.1:8501
```

---

## 📈 Performance Tips

| Issue | Solution |
|-------|----------|
| **Slow API responses** | Use `gpt-3.5-turbo` instead of `gpt-4` |
| **Slow embeddings** | Use pre-computed vectors (already done) |
| **Memory usage** | Restart containers or reduce `CHUNK_SIZE` |
| **Timeout errors** | Increase `LLM_TIMEOUT` in config.py |

---

## 🎓 Understanding the Code

### document_ingestion.py
Loads PDFs, chunks text, creates embeddings, stores in ChromaDB

### rag_system.py
Uses LangChain to combine retriever + LLM for Q&A

### main.py
FastAPI server that serves the RAG system via REST API

### app.py
Streamlit UI that calls the API and displays results

### utils.py
Helper functions for config, logging, stats

---

## 📋 Sample Test Queries

Your chatbot should answer:

1. **"What is the annual leave policy at SWS AI?"**
   - Source: SWS-AI-leave-policy.pdf
   - Expected: 20-30 days of annual leave

2. **"How many days of sick leave do employees get?"**
   - Source: SWS-AI-hr-policy.pdf
   - Expected: 10 days per year

3. **"What is the notice period for resignation?"**
   - Source: SWS-AI-resignation-policy.pdf
   - Expected: 30-60 days

4. **"What are the WFH guidelines?"**
   - Source: SWS-AI-wfh-policy.pdf
   - Expected: 2-3 days per week

5. **"Does SWS AI offer health insurance?"**
   - Source: SWS-AI-benefits-compensation.pdf
   - Expected: Yes, with details

---

## 🚀 Next Steps

### Immediate (Today)
✅ Run `setup.bat` or `bash setup.sh`
✅ Add OpenAI API key to `.env`
✅ Start `python main.py`
✅ Start `streamlit run app.py`
✅ Ask test questions

### Short Term (This Week)
- Fine-tune retrieval (adjust k, chunk size)
- Add conversation persistence
- Set up conversation logging
- Deploy to cloud (AWS/GCP/Azure)

### Long Term (This Month)
- Add document upload feature
- Implement user authentication
- Add document management UI
- Monitor performance and optimize

---

## 📞 Support Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Streamlit Docs:** https://docs.streamlit.io/
- **LangChain Docs:** https://python.langchain.com/
- **ChromaDB Docs:** https://docs.trychroma.com/
- **OpenAI Docs:** https://platform.openai.com/docs/

---

## ✨ Project Complete!

You now have a **production-ready RAG chatbot** that:

✅ Loads and processes 10 PDF documents
✅ Creates intelligent embeddings with Sentence Transformers
✅ Retrieves relevant context from ChromaDB
✅ Generates accurate answers with GPT-3.5/4
✅ Serves via REST API (FastAPI)
✅ Provides beautiful UI (Streamlit)
✅ Shows source documents for transparency
✅ Scales with more documents easily

**Estimated time to production: < 30 minutes!**

---

Built with ❤️ using **LangChain, FastAPI, ChromaDB, SentenceTransformers, and Streamlit**
