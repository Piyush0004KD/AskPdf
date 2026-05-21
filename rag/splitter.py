from langchain_text_splitters import RecursiveCharacterTextSplitter
MIN_CHUNK_LENGTH = 50

def split(text:str)-> list[str]:

    if not text or text.strip():
        raise ValueError("Cannot split empty text")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500 ,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)
    return  [chunk.strip() for chunk in chunks if len(chunk.strip())>MIN_CHUNK_LENGTH]