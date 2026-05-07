"""
Document ingestion pipeline for loading PDFs and creating embeddings
"""
import os
import glob
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
from langchain.schema import Document


class DocumentIngestionPipeline:
    """Handles PDF loading, chunking, and embedding storage"""
    
    def __init__(
        self,
        pdf_directory: str = ".",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db"
    ):
        self.pdf_directory = pdf_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize vector store
        self.vector_store = None
    
    def load_all_pdfs(self) -> List[Document]:
        """Load all PDF files from the directory"""
        pdf_files = glob.glob(os.path.join(self.pdf_directory, "*.pdf"))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {self.pdf_directory}")
        
        all_documents = []
        print(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            try:
                print(f"Loading: {os.path.basename(pdf_file)}")
                loader = PyPDFLoader(pdf_file)
                documents = loader.load()
                
                # Add source metadata
                for doc in documents:
                    doc.metadata["source"] = os.path.basename(pdf_file)
                
                all_documents.extend(documents)
            except Exception as e:
                print(f"Error loading {pdf_file}: {str(e)}")
        
        print(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        print(f"Chunking {len(documents)} documents...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, chunks: List[Document]) -> Chroma:
        """Create ChromaDB vector store from chunks"""
        print(f"Creating vector store with {len(chunks)} chunks...")
        
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="company_docs"
        )
        
        # Persist the data
        self.vector_store.persist()
        print(f"Vector store created and persisted to {self.persist_directory}")
        
        return self.vector_store
    
    def load_vector_store(self) -> Chroma:
        """Load existing vector store from disk"""
        if not os.path.exists(self.persist_directory):
            raise ValueError(f"Vector store not found at {self.persist_directory}")
        
        print(f"Loading vector store from {self.persist_directory}...")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="company_docs"
        )
        return self.vector_store
    
    def ingest_documents(self) -> Chroma:
        """Complete pipeline: Load PDFs -> Chunk -> Embed -> Store"""
        documents = self.load_all_pdfs()
        chunks = self.chunk_documents(documents)
        vector_store = self.create_vector_store(chunks)
        return vector_store
    
    def search(self, query: str, k: int = 3) -> List[Document]:
        """Search for relevant documents"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results


def initialize_pipeline(
    pdf_directory: str = ".",
    rebuild: bool = False
) -> Chroma:
    """Initialize or load the document ingestion pipeline"""
    
    pipeline = DocumentIngestionPipeline(pdf_directory=pdf_directory)
    
    # Check if vector store already exists
    if rebuild or not os.path.exists(pipeline.persist_directory):
        print("Creating new vector store...")
        vector_store = pipeline.ingest_documents()
    else:
        print("Loading existing vector store...")
        vector_store = pipeline.load_vector_store()
    
    return vector_store
