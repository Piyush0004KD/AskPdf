from fastapi import FastAPI
from routers import ingest, query

app = FastAPI(
    title="AskPDF RAG Service",
    description="RAG pipeline for document Q&A",
    version="1.0.0"
)

app.include_router(ingest.router, prefix="/rag", tags=["Ingestion"])
app.include_router(query.router, prefix="/rag", tags=["Query"])

@app.get("/")
def health_check():
    return {"status": "running", "service": "AskPDF RAG"}