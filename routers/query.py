from http.client import HTTPException
from models.schemas import QueryRequest, QueryResponse
from  rag.chain import ask
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        answer = ask(request.question, request.username)
        return QueryResponse(
            question=request.question,
            answer=answer,
            username=request.username
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )