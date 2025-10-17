"""
config.py - Configuration management for the portfolio terminal
"""
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Config:
    """Application configuration"""
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # ChromaDB Settings
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    COLLECTION_NAME: str = "portfolio_resume"
    
    # RAG Settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 3
    
    # File Paths
    RESUME_PDF_PATH: str = "./resume.pdf"
    
    # Terminal Settings
    TERMINAL_PROMPT: str = "neema@portfolio:~$ "
    TERMINAL_USER: str = "Neema Mwende"
    TERMINAL_TITLE: str = "Software & AI Engineer"
    
    def validate(self) -> bool:
        """Validate required configurations"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return True

# Global config instance
config = Config()