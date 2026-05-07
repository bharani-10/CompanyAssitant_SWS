"""
FastAPI backend for the RAG chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv
import logging

from document_ingestion import initialize_pipeline
from rag_system import create_rag_system
from langchain.chat_models import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Company Assistant Chatbot API",
    description="RAG-based chatbot for company policy questions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for vector store and RAG system
vector_store = None
rag_system = None

# Pydantic models
class ChatRequest(BaseModel):
    question: str
    
class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]


class HealthResponse(BaseModel):
    status: str
    message: str


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    global vector_store, rag_system
    
    try:
        logger.info("Initializing document pipeline...")
        # Get the directory where PDFs are stored (current working directory by default)
        pdf_dir = os.getenv("PDF_DIRECTORY", ".")
        
        vector_store = initialize_pipeline(pdf_directory=pdf_dir, rebuild=False)
        logger.info("Vector store loaded successfully")
        
        logger.info("Initializing RAG system...")
        llm_model = os.getenv("LLM_MODEL", "gemini-pro")
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        llm_provider = os.getenv("LLM_PROVIDER", "gemini")
        
        # Get appropriate API key based on provider
        if llm_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
        else:
            api_key = os.getenv("OPENAI_API_KEY")
        
        rag_system = create_rag_system(
            vector_store=vector_store,
            llm_model=llm_model,
            temperature=temperature,
            api_key=api_key,
            llm_provider=llm_provider
        )
        logger.info("RAG system initialized successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "Company Assistant Chatbot API",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    if vector_store is not None and rag_system is not None:
        return HealthResponse(
            status="healthy",
            message="All systems operational"
        )
    else:
        return HealthResponse(
            status="unhealthy",
            message="Systems not initialized"
        )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat endpoint for answering questions
    
    Args:
        request: ChatRequest with 'question' field
        
    Returns:
        ChatResponse with 'answer' and 'sources' fields
    """
    
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system not initialized"
        )
    
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        logger.info(f"Processing question: {request.question}")
        answer, sources = rag_system.answer_question(request.question)
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.get("/documents", tags=["Documents"])
async def get_documents_info():
    """Get information about loaded documents"""
    if vector_store is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not initialized"
        )
    
    try:
        # Get collection info
        collection = vector_store._collection
        count = collection.count()
        
        return {
            "total_chunks": count,
            "vector_dimension": len(vector_store._embedding_function.embed_query("test")),
            "status": "ready"
        }
    except Exception as e:
        logger.error(f"Error getting document info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting document info: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
