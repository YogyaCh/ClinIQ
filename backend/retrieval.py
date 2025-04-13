import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

from logger import get_logger, log_timing

logger = get_logger()
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

DATA_DIR = "data/reference_knowledge"
DB_DIR = "data/chroma_db"

@log_timing
def ingest_knowledgebase():
    """
    Loads and splits reference medical knowledge files and stores them in ChromaDB.
    Logs each step for traceability.
    """
    try:
        documents = []
        loaded_files = []

        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".txt"):
                path = os.path.join(DATA_DIR, filename)
                loader = TextLoader(path)
                documents.extend(loader.load())
                loaded_files.append(filename)

        logger.info(f"Loaded {len(loaded_files)} files: {loaded_files}")

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        logger.info(f"🔍 Total chunks created: {len(chunks)}")

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=EMBEDDING_MODEL,
            persist_directory=DB_DIR
        )
        vectordb.persist()
        logger.info(" ChromaDB updated and persisted.")
        return vectordb

    except Exception as e:
        logger.error(f" Error during knowledgebase ingestion: {e}")
        raise e

@log_timing
def get_contextual_knowledge(query: str, k: int = 3, task_id="") -> str:
    """
    Returns the top-k relevant chunks of knowledge based on a user query.
    Logs query, retrieved results, and failures.
    """
    try:
        logger.info(f"[{task_id}] Query: '{query}' (top {k})")
        vectordb = Chroma(
            embedding_function=EMBEDDING_MODEL,
            persist_directory=DB_DIR
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": k})
        docs = retriever.get_relevant_documents(query)
        logger.info(f"[{task_id}] Retrieved {len(docs)} documents for query.")
        context = "\n".join([doc.page_content for doc in docs])
        return context

    except Exception as e:
        logger.error(f"[{task_id}] Retrieval failed for query '{query}': {e}")
        raise e
