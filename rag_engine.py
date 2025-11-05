"""
RAG Engine for Resume-based Q&A
Author: Neema Mwende
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA  # ✅ updated import


class ResumeRAG:
    def __init__(self, resume_path, openai_api_key):
        """Initialize the RAG engine with resume file"""
        self.resume_path = resume_path
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.vectorstore = None
        self.qa_chain = None
        self._setup_rag()
    
    def _setup_rag(self):
        """Load, split, embed, and create retrieval chain"""
        # Load resume
        loader = PyPDFLoader(self.resume_path)
        documents = loader.load()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings
        )
        
        # Create retrieval chain
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # ⚙️ optional update

        # Custom prompt for first-person, bullet-point responses
        prompt_template = """You are Neema Mwende. Answer questions about yourself ONLY using information from your resume provided in the context below.

STRICT RULES:
1. Respond in FIRST PERSON (I, my, me) - you ARE Neema
2. Format responses as BULLET POINTS using the • symbol
3. ONLY use information directly from the resume context - DO NOT make up or infer anything
4. Keep responses concise and terminal-friendly
5. If the information is not in the context, say "That information is not in my resume."

Context from resume: {context}

Question: {question}

Answer (in first person, bullet points):"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # ✅ use new style for RetrievalQA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
    
    def query(self, question):
        """Query the RAG system"""
        if not self.qa_chain:
            return "RAG engine not initialized."
        
        try:
            result = self.qa_chain.invoke({"query": question})
            return result["result"]
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def get_static_response(self, command):
        """Handle static commands that don't need RAG"""
        static_commands = {
            "help": """Available commands:
• about - Learn about me
• skills - View my technical skills
• projects - See my projects
• experience - View my work experience
• education - See my education background
• contact - Get my contact information
• clear - Clear terminal
• Or ask any question about my background!""",
            "contact": """Contact Information:
• Email: neemamwende@gmail.com
• GitHub: github.com/NeemaMwende
• LinkedIn: linkedin.com/in/neemamwende""",
        }
        return static_commands.get(command.lower(), None)
