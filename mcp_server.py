"""
MCP Server - Model Context Protocol server for portfolio terminal
Exposes tools and connects backend to frontend
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
        """Initialize RAG engine and tools"""
        try:
            # Get API keys
            openai_key = os.getenv("OPENAI_API_KEY")
            gemini_key = os.getenv("GEMINI_API_KEY")
            
            if not openai_key:
                print("⚠ Warning: OPENAI_API_KEY not found")
                raise ValueError("OPENAI_API_KEY not found in environment")
            if not gemini_key:
                print("⚠ Warning: GEMINI_API_KEY not found")
                raise ValueError("GEMINI_API_KEY not found in environment")
            
            # Initialize RAG engine
            print("Initializing RAG engine...")
            self.rag_engine = RAGEngine(openai_api_key=openai_key)
            
            # Check if resume exists
            if not os.path.exists(self.resume_pdf_path):
                raise FileNotFoundError(f"Resume PDF not found at {self.resume_pdf_path}")
            
            # Load and embed resume
            print(f"Loading resume from {self.resume_pdf_path}...")
            chunk_count = self.rag_engine.load_and_embed_resume(self.resume_pdf_path)
            print(f"✓ Resume loaded and embedded ({chunk_count} chunks)")
            
            # Initialize tools
            print("Initializing portfolio tools...")
            self.tools = PortfolioTools(self.rag_engine, gemini_api_key=gemini_key)
            print("✓ Portfolio tools initialized")
            
            self.initialized = True
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
            # Commands like help/welcome are not AI-generated
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
            self.rag_engine.reset_collection()
            chunk_count = self.rag_engine.load_and_embed_resume(self.resume_pdf_path)
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
            "resume_exists": os.path.exists(self.resume_pdf_path)
        }