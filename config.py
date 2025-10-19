# """
# config.py - Configuration management for the portfolio terminal
# """
# import os
# from dotenv import load_dotenv
# from dataclasses import dataclass

# load_dotenv()

# @dataclass
# class Config:
#     """Application configuration"""
#     # API Keys
#     GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
#     OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
#     # ChromaDB Settings
#     CHROMA_PERSIST_DIR: str = "./chroma_db"
#     COLLECTION_NAME: str = "portfolio_resume"
    
#     # RAG Settings
#     CHUNK_SIZE: int = 500
#     CHUNK_OVERLAP: int = 50
#     TOP_K_RESULTS: int = 3
    
#     # File Paths
#     RESUME_PDF_PATH: str = "./resume.pdf"
    
#     # Terminal Settings
#     TERMINAL_PROMPT: str = "neema@portfolio:~$ "
#     TERMINAL_USER: str = "Neema Mwende"
#     TERMINAL_TITLE: str = "Software & AI Engineer"
    
#     def validate(self) -> bool:
#         """Validate required configurations"""
#         if not self.OPENAI_API_KEY:
#             raise ValueError("OPENAI_API_KEY not found in environment")
#         return True

# # Global config instance
# config = Config()  

"""
Configuration file for portfolio terminal
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Resume settings
    RESUME_PDF_PATH = os.getenv("RESUME_PDF_PATH", "resume.pdf")
    
    # RAG settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
    N_RESULTS = int(os.getenv("N_RESULTS", "3"))
    
    # ChromaDB settings
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "resume_collection")
    
    # UI settings
    TERMINAL_PROMPT = os.getenv("TERMINAL_PROMPT", "neema@portfolio:~$ ")
    TERMINAL_COLOR = os.getenv("TERMINAL_COLOR", "#00ff99")
    PROMPT_COLOR = os.getenv("PROMPT_COLOR", "#00aaff")
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """Validate configuration"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not set")
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY not set")
        
        if not os.path.exists(cls.RESUME_PDF_PATH):
            errors.append(f"Resume PDF not found at {cls.RESUME_PDF_PATH}")
        
        return len(errors) == 0, errors