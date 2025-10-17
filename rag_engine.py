"""
RAG Engine - Handles PDF embedding, ChromaDB storage and retrieval
"""
import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings


class RAGEngine:
    def __init__(self, openai_api_key: str = None):
        """Initialize RAG Engine with OpenAI embeddings and ChromaDB"""
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key,
            model="text-embedding-3-small"
        )
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Create or get collection
        self.collection_name = "resume_collection"
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def load_and_embed_resume(self, pdf_path: str = "resume.pdf"):
        """Load resume PDF, split into chunks, and store in ChromaDB"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Resume PDF not found at {pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        
        # Prepare data for ChromaDB
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [{"source": pdf_path, "chunk_id": i} for i in range(len(chunks))]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Generate embeddings
        embeddings_list = self.embeddings.embed_documents(texts)
        
        # Store in ChromaDB
        self.collection.add(
            embeddings=embeddings_list,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(chunks)
    
    def query_resume(self, query: str, n_results: int = 3) -> List[Dict]:
        """Query ChromaDB for relevant resume information"""
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return formatted_results
    
    def reset_collection(self):
        """Clear and reset the collection"""
        self.chroma_client.delete_collection(self.collection_name)
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )