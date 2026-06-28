# VoiceRAG

VoiceRAG is an Agentic Retrieval-Augmented Generation (RAG) API built with FastAPI. It is designed to ingest and query call transcripts using advanced AI capabilities powered by LangChain and xAI (Grok) models.

## Features

- **Agentic RAG Pipeline**: Ingest call transcripts, retrieve relevant context, and answer complex queries using a LangChain-based agent.
- **FastAPI Backend**: High-performance asynchronous API for auth, transcripts management, and querying.
- **Database**: PostgreSQL integration for relational data (users, transcript metadata).
- **Vector Store**: ChromaDB integration for efficient similarity search over transcripts.
- **Authentication**: JWT-based authentication for secure endpoints.
- **Dockerized**: Easy setup and deployment using Docker and Docker Compose.

## Tech Stack

- **Framework**: FastAPI (Python 3)
- **Database**: PostgreSQL (SQLAlchemy + psycopg2)
- **AI/LLM**: LangChain, xAI (Grok API), OpenAI compatibility
- **Embeddings**: sentence-transformers
- **Vector DB**: ChromaDB
- **Containerization**: Docker, Docker Compose

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- Or, Python 3.9+ if running locally without Docker.

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd voicerag
```

### 2. Configure Environment Variables

Copy the `.env.example` file to create a `.env` file:

```bash
cp .env.example .env
```

Open the `.env` file and configure your variables, especially your `XAI_API_KEY`:

```env
DATABASE_URL=postgresql://voicerag:password123@db:5432/voicerag
SECRET_KEY=supersecretkey-please-change-in-production
XAI_API_KEY=your_xai_api_key_here
```
*(Note: If running locally without Docker, ensure `DATABASE_URL` points to `localhost` instead of `db`)*

### 3. Run with Docker Compose

The easiest way to get started is using Docker Compose, which spins up both the FastAPI application and the PostgreSQL database.

```bash
docker-compose up -d --build
```

The API will now be available at `http://localhost:8000`.

## API Documentation

Once the application is running, FastAPI provides interactive API documentation automatically:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```text
voicerag/
├── app/
│   ├── api/         # FastAPI routers (auth, transcripts, query endpoints)
│   ├── core/        # Core configuration and security
│   ├── db/          # Database setup, models, and sessions
│   ├── rag/         # RAG pipeline logic (agent, ingestion, retriever, prompts)
│   └── main.py      # FastAPI application entry point
├── data/            # Local data storage (e.g., ChromaDB persistence)
├── .env.example     # Template for environment variables
├── docker-compose.yml
├── Dockerfile
└── requirements.txt # Python dependencies
```

## Endpoints Overview

- `POST /login` - Authenticate and receive JWT token.
- `POST /transcripts` - Upload and ingest new call transcripts.
- `GET /transcripts` - List uploaded transcripts.
- `POST /query` - Ask questions about the uploaded transcripts using the Agentic RAG pipeline.

## Development (Local without Docker)

If you prefer to run the application locally without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have a running PostgreSQL database and update your `.env` `DATABASE_URL` to point to it (e.g. `localhost`).
4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
