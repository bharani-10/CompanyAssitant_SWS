"""
Utility functions for the RAG chatbot
"""
import os
from pathlib import Path
import json
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manage configuration from environment and files"""
    
    @staticmethod
    def get_config() -> Dict[str, str]:
        """Get all configuration from environment"""
        return {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "llm_model": os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "api_host": os.getenv("API_HOST", "0.0.0.0"),
            "api_port": int(os.getenv("API_PORT", "8000")),
            "api_url": os.getenv("API_URL", "http://localhost:8000"),
            "pdf_directory": os.getenv("PDF_DIRECTORY", "."),
            "chroma_persist_directory": os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db"),
        }
    
    @staticmethod
    def validate_config() -> bool:
        """Validate that required config is present"""
        config = ConfigManager.get_config()
        
        if not config["openai_api_key"]:
            logger.error("OPENAI_API_KEY not set in environment")
            return False
        
        pdf_dir = config["pdf_directory"]
        if not os.path.exists(pdf_dir):
            logger.error(f"PDF directory not found: {pdf_dir}")
            return False
        
        pdf_files = list(Path(pdf_dir).glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return False
        
        logger.info(f"Config validated. Found {len(pdf_files)} PDF files")
        return True


class DocumentStats:
    """Get statistics about loaded documents"""
    
    @staticmethod
    def get_pdf_info(pdf_directory: str = ".") -> Dict:
        """Get info about PDF files"""
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        
        stats = {
            "total_pdfs": len(pdf_files),
            "files": [],
            "total_size_mb": 0
        }
        
        for pdf_file in sorted(pdf_files):
            size_bytes = os.path.getsize(pdf_file)
            size_mb = size_bytes / (1024 * 1024)
            
            stats["files"].append({
                "name": pdf_file.name,
                "size_mb": round(size_mb, 2)
            })
            stats["total_size_mb"] += size_mb
        
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        return stats


class ConversationLogger:
    """Log conversations for analysis"""
    
    def __init__(self, log_directory: str = "./conversation_logs"):
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)
    
    def log_interaction(self, question: str, answer: str, sources: List[Dict]):
        """Log a Q&A interaction"""
        timestamp = datetime.now().isoformat()
        
        interaction = {
            "timestamp": timestamp,
            "question": question,
            "answer": answer,
            "sources": sources,
            "answer_length": len(answer)
        }
        
        # Log to JSON file
        log_file = os.path.join(
            self.log_directory,
            f"conversations_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        )
        
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(interaction) + "\n")
        except Exception as e:
            logger.error(f"Error logging interaction: {str(e)}")


class PromptTemplates:
    """Pre-defined prompt templates for different scenarios"""
    
    @staticmethod
    def get_system_prompt() -> str:
        """System prompt for the chatbot"""
        return """You are the SWS AI Company Assistant, an AI chatbot trained to answer questions about company policies, procedures, and guidelines.

Your role:
1. Answer questions based ONLY on the provided company documents
2. Be helpful, friendly, and professional
3. If you don't have the information in the documents, clearly state that
4. Always cite which documents you referenced
5. For ambiguous questions, ask for clarification
6. Maintain confidentiality of company information"""
    
    @staticmethod
    def get_context_prompt() -> str:
        """Context prompt for RAG"""
        return """Use the following context from company documents to answer the user's question.
        
Context:
{context}

If the answer is not found in the provided context, respond with:
"I don't have that information in the company documents. Please check with HR or your manager."

Always mention which specific policy documents you referenced."""
    
    @staticmethod
    def get_summarization_prompt() -> str:
        """Prompt for summarizing documents"""
        return """Summarize the following company policy in 2-3 sentences:

{content}

Summary:"""


class QueryAnalyzer:
    """Analyze and categorize user queries"""
    
    @staticmethod
    def categorize_query(question: str) -> str:
        """Categorize a question"""
        question_lower = question.lower()
        
        categories = {
            "leave": ["leave", "vacation", "sick", "time off", "holiday"],
            "hr": ["hr", "human resources", "employee", "personnel"],
            "security": ["security", "password", "data", "access", "auth"],
            "conduct": ["conduct", "policy", "rules", "guidelines"],
            "benefits": ["benefits", "insurance", "compensation", "salary"],
            "wfh": ["work from home", "wfh", "remote", "office"],
            "onboarding": ["onboarding", "joining", "new employee", "induction"],
            "performance": ["performance", "review", "evaluation", "assessment"],
        }
        
        for category, keywords in categories.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        
        return "general"
    
    @staticmethod
    def get_answer_instructions(category: str) -> str:
        """Get special instructions based on query category"""
        instructions = {
            "leave": "Provide specific numbers and conditions for leave entitlements.",
            "security": "Emphasize security best practices and compliance requirements.",
            "benefits": "Include all applicable benefits and how to access them.",
            "wfh": "Mention specific WFH guidelines and approval processes.",
        }
        
        return instructions.get(category, "Provide accurate and helpful information.")


def print_startup_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║   🤖 SWS AI Company Assistant Chatbot       ║
    ║   RAG-Powered Employee Support System       ║
    ╚══════════════════════════════════════════════╝
    """
    print(banner)
    config = ConfigManager.get_config()
    print(f"📦 LLM Model: {config['llm_model']}")
    print(f"🗄️  PDF Directory: {config['pdf_directory']}")
    print(f"💾 Vector Store: {config['chroma_persist_directory']}")
    print("")


if __name__ == "__main__":
    # Test utilities
    print_startup_banner()
    
    print("Configuration:")
    config = ConfigManager.get_config()
    for key, value in config.items():
        if "api_key" in key:
            value = "***REDACTED***"
        print(f"  {key}: {value}")
    
    print("\nPDF Files:")
    stats = DocumentStats.get_pdf_info()
    print(f"  Total PDFs: {stats['total_pdfs']}")
    print(f"  Total Size: {stats['total_size_mb']} MB")
    for file_info in stats["files"]:
        print(f"    - {file_info['name']} ({file_info['size_mb']} MB)")
