# ai_engine.py - Handles AI-powered command suggestions using Gemini 2.5 via Byllm
import google.generativeai as genai
from typing import Generator

class AITerminalEngine:
    def __init__(self, api_key: str = None): # type: ignore
        """Initialize Gemini 2.5 Flash through Byllm"""
        if api_key is None:
            import os
            api_key = os.getenv("GEMINI_API_KEY")
        
        genai.configure(api_key=api_key) # type: ignore
        self.model = genai.GenerativeModel('gemini-2.5-flash') # type: ignore
        
        # Define user resume data
        self.resume_data = {
            "name": "Mark Gatere",
            "title": "Software & AI Engineer",
            "bio": "Passionate about building intelligent systems and modern web apps.",
            "about": "I'm Mark Gatere, passionate about building intelligent systems and modern web apps.",
            "contact": {
                "email": "markgatere@example.com",
                "github": "github.com/markgatere",
                "linkedin": "linkedin.com/in/markgatere",
                "twitter": "@markgatere"
            },
            "skills": {
                "programming": ["Python", "JavaScript", "Java", "C++"],
                "web": ["Streamlit", "React", "Next.js", "FastAPI"],
                "ai_ml": ["TensorFlow", "PyTorch", "Scikit-learn"],
                "cloud": ["AWS", "GCP", "Docker", "Kubernetes"],
                "databases": ["PostgreSQL", "MongoDB", "Firebase"]
            },
            "experience": [
                {
                    "role": "Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2022-Present",
                    "description": "Led development of ML pipeline systems, Built scalable microservices"
                },
                {
                    "role": "AI Developer",
                    "company": "StartupXYZ",
                    "duration": "2020-2022",
                    "description": "Developed NLP models, Deployed production AI systems"
                },
                {
                    "role": "Research Assistant",
                    "company": "University Lab",
                    "duration": "2019-2020",
                    "description": "Computer Vision research"
                }
            ],
            "education": [
                {
                    "degree": "BSc in Software Engineering",
                    "school": "Strathmore University",
                    "year": "2020"
                },
                {
                    "degree": "Advanced Machine Learning Certificate",
                    "school": "Coursera",
                    "year": "2021"
                },
                {
                    "degree": "Full Stack Development Bootcamp",
                    "school": "TechAcademy",
                    "year": "2019"
                }
            ],
            "certifications": [
                "AWS Certified Developer Associate",
                "TensorFlow Developer Certificate",
                "Azure AI Engineer Associate",
                "Google Cloud Certified Associate Cloud Engineer"
            ],
            "projects": [
                {
                    "name": "AI Portfolio Terminal",
                    "description": "Interactive terminal-based portfolio",
                    "tech": "Streamlit, Python, Gemini API"
                },
                {
                    "name": "MyTech API Dashboard",
                    "description": "Real-time data visualization platform",
                    "tech": "React, FastAPI, PostgreSQL"
                },
                {
                    "name": "Trading Bot Platform",
                    "description": "Automated trading system",
                    "tech": "Python, TensorFlow, AWS"
                },
                {
                    "name": "Data Analysis Tool",
                    "description": "Python-based analytics suite",
                    "tech": "Python, Pandas, Scikit-learn"
                }
            ],
            "leadership": [
                "Tech Lead at AI Club - Mentoring 50+ students",
                "Mentor at Local Developer Community",
                "Speaker at Tech Meetups",
                "Open Source Contributor"
            ]
        }
    
    def extract_data_from_resume(self, query: str) -> Generator[str, None, None]:
        """Extract specific data from resume based on user query - NO outside insights"""
        
        system_prompt = f"""You are a data extraction assistant for a portfolio terminal. 
Your ONLY job is to extract and return information from the provided resume data.
DO NOT provide any outside insights, opinions, or information not in the provided data.
DO NOT elaborate beyond what is in the data.
DO NOT provide career advice or predictions.
ONLY return the specific information requested from the resume.

Here is the complete resume data:
{str(self.resume_data)}

Extract ONLY the requested information from this data. If information is not in the data, say "Information not available in resume."
Be concise and only return what was asked for."""

        prompt = f"""Extract and return information for this query: '{query}'
Return ONLY the relevant information from the resume data provided."""

        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\n{prompt}",
                stream=True,
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error processing query: {str(e)}"
    
    def format_resume_data(self, field: str) -> str:
        """Directly return formatted resume data without AI"""
        field = field.lower().strip()
        
        if field == "name":
            return self.resume_data["name"]
        elif field == "title":
            return self.resume_data["title"]
        elif field == "contact":
            contact = self.resume_data["contact"]
            return f"""Contact Information:
Email: {contact['email']}
GitHub: {contact['github']}
LinkedIn: {contact['linkedin']}
Twitter: {contact['twitter']}"""
        elif field == "skills":
            skills = self.resume_data["skills"]
            text = "Technical Skills:\n\n"
            for category, items in skills.items():
                text += f"{category.replace('_', ' ').title()}:\n"
                text += "  " + ", ".join(items) + "\n\n"
            return text
        elif field == "experience":
            exp = self.resume_data["experience"]
            text = "Work Experience:\n\n"
            for e in exp:
                text += f"{e['role']} at {e['company']}\n"
                text += f"({e['duration']})\n"
                text += f"{e['description']}\n\n"
            return text
        elif field == "education":
            edu = self.resume_data["education"]
            text = "Education:\n\n"
            for e in edu:
                text += f"{e['degree']}\n"
                text += f"{e['school']} ({e['year']})\n\n"
            return text
        elif field == "projects":
            proj = self.resume_data["projects"]
            text = "Projects:\n\n"
            for p in proj:
                text += f"• {p['name']}\n"
                text += f"  {p['description']}\n"
                text += f"  Tech: {p['tech']}\n\n"
            return text
        elif field == "certifications":
            cert = self.resume_data["certifications"]
            text = "Certifications:\n\n"
            for c in cert:
                text += f"• {c}\n"
            return text
        elif field == "leadership":
            lead = self.resume_data["leadership"]
            text = "Leadership & Community:\n\n"
            for l in lead:
                text += f"• {l}\n"
            return text
        else:
            return "Information not available."
    
    def validate_and_extract(self, user_query: str) -> Generator[str, None, None]:
        """Validate query and extract only resume data - strict extraction mode"""
        
        query_lower = user_query.lower().strip()
        
        # Map common queries to resume fields
        field_mapping = {
            "about": "about",
            "name": "name",
            "title": "title",
            "contact": "contact",
            "skills": "skills",
            "experience": "experience",
            "education": "education",
            "projects": "projects",
            "certifications": "certifications",
            "leadership": "leadership",
            "email": "contact",
            "github": "contact",
            "linkedin": "contact",
            "work": "experience",
            "qualifications": "education",
            "certs": "certifications",
            "community": "leadership"
        }
        
        # Find matching field
        matched_field = None
        for key, field in field_mapping.items():
            if key in query_lower:
                matched_field = field
                break
        
        if matched_field:
            # Direct extraction without AI
            result = self.format_resume_data(matched_field)
            yield result
        else:
            # For ambiguous queries, use AI with strict extraction
            for chunk in self.extract_data_from_resume(user_query):
                yield chunk