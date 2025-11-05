# """
# Tools - Portfolio command handlers using RAG
# """
# from typing import Dict, Any
# from rag_engine import RAGEngine
# import google.generativeai as genai
# import os

# class PortfolioTools:
#     def __init__(self, rag_engine: RAGEngine, gemini_api_key: str = None): # type: ignore
#         """Initialize portfolio tools with RAG engine and Gemini"""
#         self.rag_engine = rag_engine
        
#         if gemini_api_key is None:
#             gemini_api_key = os.getenv("GEMINI_API_KEY")
        
#         genai.configure(api_key=gemini_api_key) # type: ignore
#         self.model = genai.GenerativeModel('gemini-2.5-flash-exp') # type: ignore
        
#         # Command mappings
#         self.command_queries = {
#             "about": "Tell me about Neema Mwende's background, bio, and professional summary",
#             "skills": "What are Neema Mwende's technical skills, programming languages, frameworks, and technologies?",
#             "experience": "What is Neema Mwende's work experience and professional roles?",
#             "projects": "What projects has Neema Mwende worked on?",
#             "education": "What is Neema Mwende's educational background and qualifications?",
#             "certifications": "What certifications does Neema Mwende have?",
#             "leadership": "What leadership roles and community involvement does Neema Mwende have?",
#             "contact": "What are Neema Mwende's contact information including email, github, linkedin, and twitter?"
#         }
    
#     def get_help(self) -> str:
#         """Return help text"""
#         return """Available commands:

# about           - Learn about me
# projects        - View my projects
# skills          - See my technical skills
# experience      - My work experience
# contact         - How to reach me
# education       - My educational background
# certifications  - View my certifications
# leadership      - Leadership and community involvement
# clear           - Clear the terminal

# Type any command to continue.."""
    
#     def get_welcome(self) -> str:
#         """Return welcome message"""
#         return """Hi, I'm Neema Mwende, a Software & AI Engineer.

# Welcome to my interactive 'AI powered' portfolio terminal!
# Type 'help' to see available commands."""
    
#     def handle_command(self, command: str) -> str:
#         """Handle portfolio commands using RAG"""
#         command = command.lower().strip()
        
#         if command == "help":
#             return self.get_help()
        
#         if command == "welcome":
#             return self.get_welcome()
        
#         if command in self.command_queries:
#             return self._query_with_rag(command)
        
#         # Handle custom queries
#         return self._query_with_rag_custom(command)
    
#     def _query_with_rag(self, command: str) -> str:
#         """Query RAG engine with predefined command"""
#         query = self.command_queries[command]
        
#         # Get relevant chunks from RAG
#         results = self.rag_engine.query_resume(query, n_results=3)
        
#         if not results:
#             return "Information not available in resume."
        
#         # Combine context
#         context = "\n\n".join([r['content'] for r in results])
        
#         # Generate response using Gemini
#         prompt = f"""Based on the following resume information, answer the query in FIRST PERSON as if you are Neema Mwende.

# Resume Context:
# {context}

# Query: {query}

# Instructions:
# - Answer in FIRST PERSON (use "I", "my", "me")
# - Be direct and concise
# - Only use information from the context provided
# - Format nicely with bullet points or sections where appropriate
# - Do NOT say "Based on the resume" or "According to the document"
# - Just answer naturally as if you are Neema speaking

# Answer:"""

#         try:
#             response = self.model.generate_content(prompt)
#             return response.text.strip()
#         except Exception as e:
#             return f"Error processing command: {str(e)}"
    
#     def _query_with_rag_custom(self, query: str) -> str:
#         """Handle custom queries using RAG"""
#         # Get relevant chunks from RAG
#         results = self.rag_engine.query_resume(query, n_results=3)
        
#         if not results:
#             return f"Command not found: '{query}'. Type 'help' for available commands."
        
#         # Combine context
#         context = "\n\n".join([r['content'] for r in results])
        
#         # Generate response using Gemini
#         prompt = f"""Based on the following resume information, answer the user's query in FIRST PERSON as if you are Neema Mwende.

# Resume Context:
# {context}

# User Query: {query}

# Instructions:
# - Answer in FIRST PERSON (use "I", "my", "me")
# - Be direct and concise
# - Only use information from the context provided
# - If the query is not related to the resume, say "Command not found. Type 'help' for available commands."
# - Do NOT say "Based on the resume" or "According to the document"
# - Just answer naturally as if you are Neema speaking

# Answer:"""

#         try:
#             response = self.model.generate_content(prompt)
#             return response.text.strip()
#         except Exception as e:
#             return f"Error processing query: {str(e)}"
