# 🤖 SWS AI Company Assistant Chatbot

A production-ready RAG (Retrieval Augmented Generation) chatbot that answers questions about company policies using LangChain, ChromaDB, and FastAPI.

## 📋 Project Overview

This chatbot uses a Retrieval Augmented Generation (RAG) approach to answer employee questions about company policies. It processes 10 company PDF documents (HR, IT Security, Leave, Benefits, etc.) and provides accurate, grounded answers sourced directly from these documents.

### Architecture

```
PDF Documents (10 files)
    ↓
Text Extraction & Chunking (RecursiveCharacterTextSplitter)
    ↓
Embeddings (SentenceTransformers)
    ↓
Vector Database (ChromaDB)
    ↓
User Question
    ↓
Question Embedding
    ↓
Similarity Search (retrieve top-3 relevant chunks)
    ↓
LLM (OpenAI/Ollama/Gemini)
    ↓
Answer + Source Documents
```

## 🛠️ Technology Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| **Language** | Python 3.8+ | Industry standard for AI/ML |
| **Backend** | FastAPI | High performance, auto-documentation |
| **Frontend** | Streamlit | Fast prototype UI, great for demos |
| **Vector DB** | ChromaDB | Simple, local, perfect for prototypes |
| **Embeddings** | Sentence Transformers | Fast, accurate, runs locally |
| **LLM Framework** | LangChain | Abstracts LLM complexity, RAG-ready |
| **LLM** | Gemini | Best quality, but Ollama work too |
| **PDF Loading** | PyPDFLoader (LangChain) | Reliable text extraction |
| **API Server** | Uvicorn | ASGI server for FastAPI |

## 📦 Project Structure

```
Company_Assistant_Chatbot/
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .env                          # Local environment config (create yourself)
├── main.py                       # FastAPI backend application
├── app.py                        # Streamlit frontend application
├── document_ingestion.py         # PDF loading and embedding pipeline
├── rag_system.py                 # RAG chain and LLM integration
├── chroma_db/                    # ChromaDB vector store (auto-created)
│   └── (vector embeddings & metadata)
├── SWS-AI-*.pdf                  # Company policy documents (10 files)
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
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenAI API key (or Ollama running locally)

### Step 1: Clone/Setup

```bash
# Navigate to project directory
cd Company_Assistant_Chatbot
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# (Use any text editor)
# OPENAI_API_KEY=sk-your-key-here
```

**If using Ollama (free, local):**
- Install Ollama from https://ollama.ai
- Run: `ollama pull ollama/neural-chat` or `ollama pull mistral`
- Update `.env`: `LLM_MODEL=ollama` and add `OLLAMA_BASE_URL=http://localhost:11434`

### Step 5: Initialize Vector Store (First Time Only)

```bash
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

This will:
1. Load all 10 PDF files
2. Extract and chunk text
3. Generate embeddings using SentenceTransformers
4. Create and persist ChromaDB vector store in `chroma_db/` folder

**Time:** ~2-5 minutes depending on your system

### Step 6: Start the Backend API

Open a terminal and run:

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**API Documentation:** Visit http://localhost:8000/docs

### Step 7: Start the Frontend (New Terminal)

```bash
# Make sure your venv is activated
streamlit run app.py
```

Streamlit will automatically open in your browser at `http://localhost:8501`

## 💬 Usage

### Via Streamlit UI (Recommended)

1. Open http://localhost:8501
2. Type a question in the input field
3. Click "Send" or press Enter
4. View the answer with source documents

### Via API (FastAPI)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the leave policy?"}'
```

Response:
```json
{
  "answer": "According to the Leave Policy, employees get 20 days of annual leave...",
  "sources": [
    {
      "source": "SWS-AI-leave-policy.pdf",
      "page": 1,
      "content": "Annual Leave: 20 days per calendar year..."
    }
  ]
}
```

### Endpoints

- **POST** `/chat` - Ask a question
- **GET** `/health` - Health check
- **GET** `/documents` - Document statistics
- **GET** `/docs` - Interactive API documentation

## 🔧 Configuration

Edit `.env` to customize:

```bash
# LLM to use (gpt-3.5-turbo, gpt-4, ollama, etc.)
LLM_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# PDF location (default: current directory)
PDF_DIRECTORY=.
```

## 📊 Key Features

✅ **Document Processing**
- Automatic PDF loading and text extraction
- Intelligent text chunking (500 tokens, 50 overlap)
- Metadata preservation (source, page number)

✅ **Retrieval Optimization**
- Semantic search using embeddings
- Top-3 chunk retrieval for context
- Duplicate detection and removal

✅ **RAG Quality**
- LLM instructions to answer only from documents
- Source attribution in every answer
- No hallucinations through grounding

✅ **Production Ready**
- FastAPI with async support
- CORS enabled for external frontends
- Error handling and logging
- Health checks and diagnostics

✅ **Beautiful UI**
- Modern Streamlit interface
- Color-coded messages
- Expandable source documents
- Easy conversation management

## 🧠 How It Works

### 1. Document Ingestion
```python
DocumentIngestionPipeline loads PDFs → Chunks text → Generates embeddings → Stores in ChromaDB
```

### 2. Query Processing
```
User Question → Embed using SentenceTransformers → Search ChromaDB (similarity) → Top-3 matches
```

### 3. Answer Generation
```
Context + Question → LLM (with grounding prompt) → Answer + Sources
```

## 🎯 Example Interactions

### Question 1
**User:** "How many days of sick leave do I get?"

**Bot:** "According to the HR Policy document, employees are entitled to 10 days of paid sick leave per calendar year. These can be used for personal illness or medical appointments."

**Sources:** HR Policy (Page 3)

### Question 2
**User:** "What's the WFH policy?"

**Bot:** "SWS AI offers flexible work-from-home arrangements. Employees can work remotely up to 3 days per week after the first 6 months of employment. Approval from direct manager is required."

**Sources:** Work From Home Policy (Page 1)

## 🐛 Troubleshooting

### "Cannot connect to API"
```bash
# Check if backend is running
# Terminal 1: Is main.py running?
# Try: http://localhost:8000/health
```

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "OPENAI_API_KEY not set"
```bash
# Check .env file exists
# Verify OPENAI_API_KEY=sk-... is uncommented
# Restart main.py
```

### "Vector store not found"
```bash
# Rebuild vector store
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

### Slow responses
- Reduce `chunk_size` in `document_ingestion.py` (speeds up search)
- Use `gpt-3.5-turbo` instead of `gpt-4` (faster LLM)
- Switch to Ollama for local inference (no API latency)

## 📈 Performance

| Metric | Value |
|--------|-------|
| **Initial Setup** | ~5 minutes |
| **Query Latency** | ~1-3 seconds with OpenAI |
| **Local Query** | ~0.5s with Ollama |
| **Vector DB Size** | ~50-100 MB |
| **Memory Usage** | ~200-300 MB |

## 🔐 Security Notes

- API keys stored in `.env` (never commit!)
- `.env` should be in `.gitignore`
- Only use HTTPS in production
- Consider rate limiting for public APIs
- Validate/sanitize user inputs

## 🚀 Deployment

### Local Testing ✅
```bash
python main.py &
streamlit run app.py
```

### Docker (Production)
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t chatbot .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY chatbot
```

## 📝 Advanced Usage

### Switch to Ollama (Free)
```bash
# Install Ollama: https://ollama.ai
ollama pull mistral

# Update main.py to use Ollama instead of OpenAI
# Change ChatOpenAI to use ollama backend
```

### Add More Documents
```bash
# Just add new PDFs to directory
# Then rebuild:
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"
```

### Tune Retrieval
Edit `document_ingestion.py`:
```python
# Adjust chunk size (larger = less relevant but faster)
chunk_size=500  

# Change number of retrieved chunks
search_kwargs={"k": 5}  # Default is 3
```

## 📚 Sample Test Queries

The chatbot should answer these:
- "What is the annual leave policy at SWS AI?"
- "How many days of sick leave do employees get?"
- "What is the notice period for resignation?"
- "What are the WFH guidelines?"
- "Does SWS AI offer health insurance?"
- "What is the password policy for company systems?"
- "How are performance reviews conducted?"
- "What tools does SWS AI use for communication?"
- "What is the code of conduct?"
- "What benefits and compensation do we offer?"

## 🎓 Learning Resources

- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [SentenceTransformers](https://www.sbert.net/)

## 📞 Support

For issues:
1. Check the Troubleshooting section
2. Review logs in terminal
3. Try rebuild: `document_ingestion.py` with `rebuild=True`
4. Check API health: `http://localhost:8000/health`

## 📄 License

This project is provided as-is for the SWS AI assessment.

---

**Built with ❤️ using LangChain, FastAPI, ChromaDB, and Streamlit**
