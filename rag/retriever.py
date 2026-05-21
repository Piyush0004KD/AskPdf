from rag.embedding import embed
from rag.vector_space import search_chunks


def retrieve(question:str , username:str , top_k:int = 5) -> list[str]:

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")
    if not username or not username.strip():
        raise ValueError("Username cannot be empty")

    question_embedding = embed(question)
    chunks = search_chunks(question_embedding,username,top_k)
    return chunks


