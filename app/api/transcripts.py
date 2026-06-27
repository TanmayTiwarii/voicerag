from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.models import User, TranscriptMetadata
from app.db.database import get_db
from app.rag.ingestion import ingest_transcript

router = APIRouter(prefix="/api/transcripts", tags=["transcripts"])

@router.post("/ingest")
async def upload_transcript(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    content = await file.read()
    text_content = content.decode("utf-8")
    
    # Save metadata to DB
    transcript_meta = TranscriptMetadata(filename=file.filename)
    db.add(transcript_meta)
    db.commit()
    db.refresh(transcript_meta)
    
    # Ingest to ChromaDB
    metadata = {"source": file.filename, "transcript_id": transcript_meta.id}
    num_chunks = ingest_transcript(text_content, metadata)
    
    return {
        "message": f"Successfully ingested transcript {file.filename}",
        "chunks_created": num_chunks
    }
