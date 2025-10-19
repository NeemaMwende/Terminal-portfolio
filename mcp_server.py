"""
MCP Server - Model Context Protocol server for portfolio terminal
OPTIMIZED: Fast initialization with caching
"""
from typing import Optional, Tuple
from rag_engine import RAGEngine
from tools import PortfolioTools
import os


class MCPServer:
    def __init__(self, resume_pdf_path: str = "resume.pdf"):
        """Initialize MCP Server with RAG and tools"""
        self.resume_pdf_path = resume_pdf_path
        self.rag_engine: Optional[RAGEngine] = None
        self.tools: Optional[PortfolioTools] = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize RAG engine and tools - FAST with caching"""
        try:
            # Get API keys
            openai_key = os.getenv("OPENAI_API_KEY")
            gemini_key = os.getenv("GEMINI_API_KEY")
            
            if not openai_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            if not gemini_key:
                raise ValueError("GEMINI_API_KEY not found in environment")
            
            # Initialize RAG engine (fast - uses cached embeddings)
            self.rag_engine = RAGEngine(
                openai_api_key=openai_key,
                persist_directory="./chroma_db"
            )
            
            # Check if resume exists
            if not os.path.exists(self.resume_pdf_path):
                raise FileNotFoundError(f"Resume PDF not found at {self.resume_pdf_path}")
            
            # Load and embed resume (FAST - only embeds if not cached)
            chunk_count = self.rag_engine.load_and_embed_resume(
                self.resume_pdf_path,
                force_reload=False  # Set to True to force re-embedding
            )
            
            # Initialize tools (fast - no heavy operations)
            self.tools = PortfolioTools(self.rag_engine, gemini_api_key=gemini_key)
            
            self.initialized = True
            print(f"✓ MCP Server ready ({chunk_count} chunks loaded)")
            return True
            
        except Exception as e:
            print(f"✗ Initialization error: {str(e)}")
            self.initialized = False
            return False
    
    def process_command(self, command: str) -> Tuple[str, bool]:
        """
        Process a command and return (response, is_ai_generated)
        
        Args:
            command: User command
            
        Returns:
            Tuple of (response_text, is_ai_generated_flag)
        """
        if not self.initialized:
            return "Error: Server not initialized. Please check your API keys.", False
        
        if not self.tools:
            return "Error: Tools not available.", False
        
        # Special handling for clear command
        if command.lower().strip() == "clear":
            return "", False
        
        # Process through tools
        try:
            response = self.tools.handle_command(command)
            
            # Determine if it's AI-generated
            basic_commands = ["help", "welcome"]
            is_ai = command.lower().strip() not in basic_commands
            
            return response, is_ai
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            return error_msg, False
    
    def reset_rag(self) -> bool:
        """Reset RAG engine and reload resume"""
        if not self.rag_engine:
            return False
        
        try:
            chunk_count = self.rag_engine.load_and_embed_resume(
                self.resume_pdf_path,
                force_reload=True
            )
            print(f"✓ RAG reset and resume reloaded ({chunk_count} chunks)")
            return True
        except Exception as e:
            print(f"✗ Reset error: {str(e)}")
            return False
    
    def health_check(self) -> dict:
        """Check server health status"""
        return {
            "initialized": self.initialized,
            "rag_engine_ready": self.rag_engine is not None,
            "tools_ready": self.tools is not None,
            "resume_exists": os.path.exists(self.resume_pdf_path),
            "cached_chunks": self.rag_engine.collection.count() if self.rag_engine else 0
        }