from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.dependencies import get_current_user
from app.db.models import User
from app.rag.agent import query_agent

router = APIRouter(prefix="/api/query", tags=["query"])

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/", response_model=QueryResponse)
def ask_question(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    # In a real app, you might want to log queries, track latency, etc.
    answer = query_agent(request.question)
    return QueryResponse(answer=answer)
