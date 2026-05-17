
def build_prompt(chunks:list[str],question:str)->str:
    context = "\n\n".join(chunks)

    prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the context provided below.
If the answer is not found in the context, say exactly: "I don't have that information in your documents."
Do not make up answers. Do not use outside knowledge.

    Context:
    {context}
    
    Question : {question}
    
    Answer:"""

    return prompt