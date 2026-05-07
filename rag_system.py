"""
RAG system for question answering using LangChain
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from typing import Dict, List, Tuple
import os


class RAGSystem:
    """RAG system for answering questions based on company documents"""
    
    def __init__(
        self,
        vector_store: Chroma,
        llm_model: str = "gemini-pro",
        temperature: float = 0.7,
        api_key: str = None,
        llm_provider: str = "gemini"
    ):
        self.vector_store = vector_store
        
        # Initialize LLM based on provider
        if llm_provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model=llm_model,
                temperature=temperature,
                google_api_key=api_key or os.getenv("GEMINI_API_KEY")
            )
        else:
            self.llm = ChatOpenAI(
                model_name=llm_model,
                temperature=temperature,
                openai_api_key=api_key or os.getenv("OPENAI_API_KEY"),
                streaming=True
            )
        
        # Create the RAG chain
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self) -> RetrievalQA:
        """Create a RetrievalQA chain"""
        
        # Custom prompt template
        prompt_template = """Use the following pieces of context to answer the user question. 
If you don't know the answer from the context provided, say "I don't have that information in the company documents."

Always cite which documents you used to answer the question.

Context:
{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create the chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa_chain
    
    def answer_question(self, question: str) -> Tuple[str, List[Dict]]:
        """Answer a question and return the answer with source documents"""
        
        result = self.qa_chain({"query": question})
        
        answer = result.get("result", "No answer generated")
        
        # Extract source documents
        source_docs = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                source_docs.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "page": doc.metadata.get("page", 0)
                })
        
        return answer, source_docs
    
    def get_retriever(self):
        """Get the retriever for advanced usage"""
        return self.vector_store.as_retriever(search_kwargs={"k": 3})


def create_rag_system(
    vector_store: Chroma,
    llm_model: str = "gemini-pro",
    temperature: float = 0.7,
    api_key: str = None,
    llm_provider: str = "gemini"
) -> RAGSystem:
    """Factory function to create a RAG system"""
    return RAGSystem(
        vector_store=vector_store,
        llm_model=llm_model,
        temperature=temperature,
        api_key=api_key,
        llm_provider=llm_provider
    )
