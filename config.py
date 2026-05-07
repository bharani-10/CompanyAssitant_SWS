"""
Template configuration file with advanced settings
"""

# ============================================
# LLM Configuration
# ============================================

# Available: gpt-4, gpt-3.5-turbo, claude-3, ollama
LLM_MODEL = "gpt-3.5-turbo"

# Temperature: 0.0 (deterministic) to 1.0 (creative)
# Lower = more factual, Higher = more creative
TEMPERATURE = 0.7

# Max tokens in response
MAX_TOKENS = 500

# ============================================
# Retrieval Configuration
# ============================================

# Number of chunks to retrieve for context
RETRIEVAL_K = 3

# Chunk size for document splitting (tokens)
CHUNK_SIZE = 500

# Overlap between chunks (tokens)
CHUNK_OVERLAP = 50

# Similarity threshold (0-1, higher = more relevant)
SIMILARITY_THRESHOLD = 0.30

# ============================================
# Embedding Configuration
# ============================================

# Embedding model: sentence-transformers/all-MiniLM-L6-v2 (fast, good)
# Other options: all-mpnet-base-v2 (better, slower)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Embedding dimension (depends on model)
EMBEDDING_DIMENSION = 384

# ============================================
# Vector Store Configuration
# ============================================

# Persist directory for ChromaDB
PERSIST_DIRECTORY = "./chroma_db"

# Collection name
COLLECTION_NAME = "company_docs"

# ============================================
# API Configuration
# ============================================

# Host
API_HOST = "0.0.0.0"

# Port
API_PORT = 8000

# Enable CORS
ENABLE_CORS = True

# ============================================
# Logging Configuration
# ============================================

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Save conversation logs
SAVE_LOGS = True
LOG_DIRECTORY = "./conversation_logs"

# ============================================
# Advanced Settings
# ============================================

# Enable response streaming
STREAMING = True

# Timeout for LLM API calls (seconds)
LLM_TIMEOUT = 30

# Retry failed requests
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds

# ============================================
# Document Processing
# ============================================

# PDF directory to scan for documents
PDF_DIRECTORY = "."

# Exclude these file patterns
EXCLUDE_PATTERNS = ["*.pyc", "__pycache__"]

# ============================================
# Security
# ============================================

# Allowed origins for CORS
CORS_ORIGINS = ["*"]

# Rate limiting (requests per minute)
RATE_LIMIT = 60

# ============================================
# Performance
# ============================================

# Use GPU if available
USE_GPU = True

# Batch size for embedding generation
BATCH_SIZE = 8

# Number of worker threads
WORKERS = 4
