from typing import cast
from openai import OpenAI
from openai.types.chat import ChatCompletion

from config import OPENAI_API_KEY
from rag.loader import load
from rag.splitter import split
from rag.embedding import embed
from rag.vector_space import save_chunks, delete_chunks
from rag.retriever import retrieve
from rag.prompt import build_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def ingestion(file_bytes:bytes,filename:str,document_id:str,username:str) :

    text = load(file_bytes,filename)
    chunks = split(text)

    for i,chunks in enumerate(chunks):
        save_chunks(document_id,username,chunks,embed(chunks),i)

    return len(chunks)

def ask(question:str , username:str) -> str:

    chunks = retrieve(question,username)
    if not chunks:
        return "I don't have that information in my documents."

    prompt = build_prompt(chunks,question)

    response = cast( ChatCompletion , client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0,
        stream=False
        ))

    if not response:
        return "We dont have answer"

    return response.choices[0].message.content or "no answer generated"


def remove_document(document_id: str, username: str):
    delete_chunks(document_id, username)