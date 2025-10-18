"""
RAG Engine - Handles PDF embedding, ChromaDB storage and retrieval
OPTIMIZED: Uses persistent storage to avoid re-embedding on every load
"""
import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
import hashlib


class RAGEngine:
    def __init__(self, openai_api_key: str = None, persist_directory: str = "./chroma_db"): # type: ignore
        """Initialize RAG Engine with OpenAI embeddings and ChromaDB"""
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        self.embeddings = OpenAIEmbeddings(
            # api_key=openai_api_key,
            # model="text-embedding-3-small"
        )
        
        # Use persistent ChromaDB
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Collection name
        self.collection_name = "resume_collection"
        
        # Try to get existing collection
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
            print(f"✓ Loaded existing collection with {self.collection.count()} documents")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print("✓ Created new collection")
    
    def get_pdf_hash(self, pdf_path: str) -> str:
        """Get hash of PDF file to detect changes"""
        with open(pdf_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def is_resume_loaded(self, pdf_path: str) -> bool:
        """Check if resume is already loaded and up-to-date"""
        try:
            # Check if collection has documents
            count = self.collection.count()
            if count == 0:
                return False
            
            # Check if PDF hash matches
            current_hash = self.get_pdf_hash(pdf_path)
            metadata = self.collection.get(limit=1)
            
            if metadata and metadata['metadatas']:
                stored_hash = metadata['metadatas'][0].get('pdf_hash')
                return stored_hash == current_hash
            
            return False
        except:
            return False
    
    def load_and_embed_resume(self, pdf_path: str = "resume.pdf", force_reload: bool = False) -> int:
        """Load resume PDF, split into chunks, and store in ChromaDB"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Resume PDF not found at {pdf_path}")
        
        # Check if already loaded
        if not force_reload and self.is_resume_loaded(pdf_path):
            count = self.collection.count()
            print(f"✓ Resume already loaded ({count} chunks) - skipping embedding")
            return count
        
        print("📄 Loading and embedding resume (first time or updated)...")
        
        # Get PDF hash for change detection
        pdf_hash = self.get_pdf_hash(pdf_path)
        
        # Clear existing data if reloading
        if self.collection.count() > 0:
            self.reset_collection()
        
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
        metadatas: List[Dict[str, Any]] = [
            {
                "source": pdf_path, 
                "chunk_id": i,
                "pdf_hash": pdf_hash
            } 
            for i in range(len(chunks))
        ]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        embeddings_list = self.embeddings.embed_documents(texts)
        
        # Store in ChromaDB
        print("💾 Storing in database...")
        self.collection.add(
            embeddings=embeddings_list, # type: ignore
            documents=texts,
            metadatas=metadatas, # type: ignore
            ids=ids
        )
        
        print(f"✓ Resume embedded and stored ({len(chunks)} chunks)")
        return len(chunks)
    
    def query_resume(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Query ChromaDB for relevant resume information"""
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results: List[Dict[str, Any]] = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return formatted_results
    
    def reset_collection(self) -> None:
        """Clear and reset the collection"""
        try:
            self.chroma_client.delete_collection(self.collection_name)
        except:
            pass
        
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print("✓ Collection reset")