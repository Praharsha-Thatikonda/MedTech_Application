import os
import json
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

class VectorStore:
    """
    Manages the Vector Database (ChromaDB) for Long-Term Memory (RAG).
    Stores embeddings of medical documents/knowledge.
    """
    def __init__(self, collection_name="medical_knowledge"):
        self.client = None
        self.collection = None
        self.collection_name = collection_name
        
        if chromadb:
            try:
                # Persistent storage in ./databases/chroma_db
                db_path = os.path.join(os.path.dirname(__file__), 'chroma_db')
                self.client = chromadb.PersistentClient(path=db_path)
                
                # Get or Create Collection
                self.collection = self.client.get_or_create_collection(name=self.collection_name)
                print(f"[VectorStore] ChromaDB initialized at {db_path}")
            except Exception as e:
                print(f"[VectorStore] Error initializing ChromaDB: {e}")
        else:
            print("[VectorStore] ChromaDB not installed. Vector search disabled.")

    def add_documents(self, documents, ids=None, metadatas=None):
        """
        Add documents to the vector store.
        documents: list of strings
        ids: list of unique IDs
        metadatas: list of dicts
        """
        if not self.collection:
            return False
            
        try:
            if not ids:
                ids = [f"doc_{i}" for i in range(len(documents))]
                
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            return True
        except Exception as e:
            print(f"[VectorStore] Error adding docs: {e}")
            return False

    def search(self, query_text, n_results=3):
        """
        Semantic search for relevant documents.
        """
        if not self.collection:
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"[VectorStore] Search error: {e}")
            return []

# Singleton
vector_store = VectorStore()
