from fastapi import APIRouter,UploadFile,File,Form
from models.schemas import IngestResponse,DeleteRequest,DeleteResponse
from rag.chain import ingestion , remove_document

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
        file:UploadFile = File(...),
        document_id:str = Form(...),
        username:str = Form(...)
):
    try:
        file_bytes = await file.read()
        chunks_saved = ingestion(file_bytes , file.filename or "unknown", document_id , username)
        return IngestResponse(document_id=document_id,
                              username=username,
                              filename=file.filename or "unknown",
                              chunks_saved=chunks_saved,
                              status="success")

    except Exception as e:
        return IngestResponse(document_id=document_id,
                              username=username,
                              filename=file.filename or "unknown",
                              chunks_saved=0,
                              status=f"failed: {str(e)}"
        )

@router.delete("/delete", response_model=DeleteResponse)
async def delete_document(request:DeleteRequest):
    try:
        remove_document(request.document_id,request.username)
        return DeleteResponse(document_id=request.document_id,
                              username=request.username,
                              status="success")
    except Exception as e:
        return DeleteResponse(document_id=request.document_id,
                              username=request.username,
                              status=f"failed: {str(e)}")