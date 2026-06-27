import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings

# Initialize embeddings model locally. We use all-MiniLM-L6-v2 for fast, decent embeddings.
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore() -> Chroma:
    """Returns the Chroma vector store instance."""
    # Ensure directory exists
    os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
    
    vectorstore = Chroma(
        collection_name="call_transcripts",
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY
    )
    return vectorstore

def get_retriever():
    """Returns a retriever interface for the vector store."""
    vectorstore = get_vectorstore()
    # We can configure search parameters here (e.g., k=4 chunks to retrieve)
    return vectorstore.as_retriever(search_kwargs={"k": 4})
