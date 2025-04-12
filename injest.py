# ingest.py

from backend.retrieval import ingest_knowledgebase

if __name__ == "__main__":
    print("📚 Ingesting reference knowledge into ChromaDB...")
    db = ingest_knowledgebase()
    print("✅ ChromaDB setup complete! Documents stored:", db._collection.count())
