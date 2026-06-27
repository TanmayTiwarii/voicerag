from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.rag.retriever import get_vectorstore

def ingest_transcript(text: str, metadata: dict = None):
    """
    Chunks a transcript and ingests it into the Chroma vector store.
    """
    if metadata is None:
        metadata = {}

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    
    # Split text into chunks
    chunks = text_splitter.create_documents([text], metadatas=[metadata])
    
    # Get vector store and add documents
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    vectorstore.persist() # Explicitly persist if needed, though Chroma does it automatically in recent versions.
    
    return len(chunks)
