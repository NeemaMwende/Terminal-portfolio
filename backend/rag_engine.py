"""
RAG Engine for Resume-based Q&A with Gemini
"""
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA


class ResumeRAG:
    def __init__(self, resume_path, gemini_api_key):
        self.resume_path = resume_path
        os.environ["GOOGLE_API_KEY"] = gemini_api_key
        self.vectorstore = None
        self.qa_chain = None
        self._setup_rag()
    
    def _setup_rag(self):
        # Load PDF
        loader = PyPDFLoader(self.resume_path)
        documents = loader.load()
        
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(documents)
        
        # Create embeddings with Gemini
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings
        )
        
        # Create LLM with Gemini
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        
        # Custom prompt
        prompt_template = """You are answering as the person in the resume. Use FIRST PERSON (I, my, me).

RULES:
1. Answer in first person
2. Use bullet points with • symbol
3. Keep responses SHORT and concise
4. ONLY use information from the context
5. If not in context, say "That information is not in my resume."

Context: {context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
    
    def query(self, question):
        if not self.qa_chain:
            return "RAG engine not initialized."
        try:
            result = self.qa_chain.invoke({"query": question})
            return result["result"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_static_response(self, command):
        static = {
            "help": """Available commands:
• about       - Learn about me
• projects    - View my projects
• skills      - See my technical skills
• experience  - My work experience
• contact     - How to reach me
• education   - My educational background
• certifications - View my certifications
• leadership  - Leadership and community involvement
• clear       - Clear the terminal

Type any command to continue..""",
        }
        return static.get(command.lower(), None)


# Test independently
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    RESUME_PATH = "resume.pdf"
    
    rag = ResumeRAG(RESUME_PATH, GEMINI_API_KEY)
    
    # Test queries
    print("Testing RAG Engine...\n")
    test_queries = ["help", "What are your skills?", "Tell me about your experience"]
    
    for q in test_queries:
        static = rag.get_static_response(q)
        if static:
            print(f"Q: {q}\nA: {static}\n")
        else:
            print(f"Q: {q}\nA: {rag.query(q)}\n")