import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from typing import Optional, List
import os

class SimpleRAG:
    def __init__(self, resume_path="data/resume.txt"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.resume_path = resume_path
        self.vectorstore = None
        self.setup()
    
    def setup(self):
        # Load resume
        if not os.path.exists(self.resume_path):
            # Create sample resume if doesn't exist
            os.makedirs("data", exist_ok=True)
            with open(self.resume_path, "w") as f:
                f.write(self._get_sample_resume())
        
        with open(self.resume_path, "r") as f:
            text = f.read()
        
        # Split text
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)
        
        # Create vectorstore
        self.vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            collection_name="resume"
        )
    
    def query(self, command: str) -> str:
        # Map commands to queries
        command_map = {
            "about": "Tell me about Mark Gatere, his background and who he is",
            "projects": "List all projects Mark has worked on with descriptions",
            "skills": "What are Mark's technical skills and technologies he knows?",
            "experience": "Describe Mark's work experience and job history",
            "contact": "How can I contact Mark? Provide contact information",
            "education": "What is Mark's educational background?",
            "certifications": "What certifications does Mark have?",
            "leadership": "Describe Mark's leadership experience and community involvement"
        }
        
        query_text = command_map.get(command.lower(), command)
        
        # Retrieve relevant context
        docs = self.vectorstore.similarity_search(query_text, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Simple response generation
        return self._generate_response(command, context)
    
    def _generate_response(self, command: str, context: str) -> str:
        # Simple rule-based responses with context
        responses = {
            "about": f"Based on my resume:\n\n{context[:500]}",
            "projects": f"Here are my key projects:\n\n{context[:600]}",
            "skills": f"My technical skills include:\n\n{context[:500]}",
            "experience": f"My work experience:\n\n{context[:600]}",
            "contact": f"Contact information:\n\n{context[:400]}",
            "education": f"Educational background:\n\n{context[:500]}",
            "certifications": f"Certifications:\n\n{context[:500]}",
            "leadership": f"Leadership & community involvement:\n\n{context[:500]}"
        }
        
        return responses.get(command.lower(), context[:500])
    
    def _get_sample_resume(self) -> str:
        return """
MARK GATERE
Software & AI Engineer
Email: mark.gatere@example.com | Phone: +254 700 123456
LinkedIn: linkedin.com/in/markgatere | GitHub: github.com/markgatere

ABOUT ME
Passionate Software & AI Engineer with 5+ years of experience building scalable applications and AI-powered solutions. 
Specialized in full-stack development, machine learning, and cloud architecture. Strong advocate for clean code and user-centric design.

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, Java, SQL
Frontend: React, Next.js, Vue.js, Tailwind CSS, Material-UI
Backend: Node.js, Django, Flask, FastAPI, Express
AI/ML: TensorFlow, PyTorch, LangChain, Hugging Face, OpenAI
Databases: PostgreSQL, MongoDB, Redis, ChromaDB
Cloud: AWS, Google Cloud, Docker, Kubernetes

WORK EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Led development of AI-powered customer service platform using LangChain and GPT-4
- Architected microservices handling 1M+ daily requests with 99.9% uptime
- Mentored team of 5 junior developers in modern development practices

Full Stack Developer | StartupXYZ | 2019 - 2021
- Built responsive web applications using React and Node.js
- Implemented RESTful APIs serving 50K+ active users
- Reduced page load times by 40% through optimization

PROJECTS

AI Chat Assistant
Full-stack chatbot using LangChain, ChromaDB, and React. Implements RAG for context-aware responses.
Tech: Python, React, LangChain, Vector DB

E-Commerce Platform
Scalable online marketplace with payment integration and real-time inventory management.
Tech: Next.js, PostgreSQL, Stripe API

EDUCATION
Bachelor of Science in Computer Science | University of Nairobi | 2015 - 2019
GPA: 3.8/4.0 | Dean's List

CERTIFICATIONS
- AWS Certified Solutions Architect
- Google Cloud Professional Developer
- Deep Learning Specialization (Coursera)

LEADERSHIP & COMMUNITY
- Founder, Nairobi AI Developers Meetup (200+ members)
- Open source contributor to React and Python projects
- Technical mentor at Code for Kenya
- Speaker at PyCon Kenya 2023
"""