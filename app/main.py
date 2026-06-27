from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.db import models

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VoiceRAG API", description="Agentic RAG Pipeline over Call Transcripts")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, transcripts, query

app.include_router(auth.router)
app.include_router(transcripts.router)
app.include_router(query.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to VoiceRAG API"}
