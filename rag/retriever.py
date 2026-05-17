from rag.embedding import embed
from rag.vector_space import search_chunks


def retrieve(question:str , username:str , top_k:int = 5) -> list[str]:

    question_embedding = embed(question)
    chunks = search_chunks(question_embedding,username,top_k)
    return chunks


