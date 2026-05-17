from pydantic import BaseModel

class IngestResponse(BaseModel):
    document_id: str
    username: str
    filename: str
    chunks_saved: int
    status: str

class QueryRequest(BaseModel):
    question:str
    username:str

class QueryResponse(BaseModel):
    question:str
    answer:str
    username:str

class DeleteRequest(BaseModel):
    document_id:str
    username:str

class DeleteResponse(BaseModel):
    document_id:str
    username:str
    status:str