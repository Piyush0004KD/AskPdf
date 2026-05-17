from fastapi import APIRouter
from models.schemas import QueryRequest, QueryResponse
from  rag.chain import ask

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
        return QueryResponse(
            question=request.question,
            answer=f"Error: {str(e)}",
            username=request.username
        )