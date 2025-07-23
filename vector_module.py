import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Optional

# Use a multilingual embedding model for better Bengali support
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

# ChromaDB persistent storage (can be set to a folder for persistence)
chroma_client = chromadb.Client(Settings())

def create_or_load_collection(name: str):
    return chroma_client.get_or_create_collection(name)

def add_documents(collection, docs: List[str], metadatas: Optional[List[dict]] = None):
    embeddings = model.encode(docs).tolist()
    ids = [f"doc_{i}" for i in range(len(docs))]
    # Ensure each metadata dict is non-empty
    metadatas = metadatas if metadatas else [{"source": "ocr"} for _ in docs]
    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_collection(collection, query: str, top_k: int = 3):
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
 
    return results 