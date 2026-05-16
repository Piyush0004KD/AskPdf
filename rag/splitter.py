from langchain_text_splitters import RecursiveCharacterTextSplitter

def split(text:str)-> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500 ,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)
    return  [chunk.strip() for chunk in chunks if chunk.strip()]