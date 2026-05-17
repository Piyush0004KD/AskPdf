import psycopg2
from config import DATABASE_URL

def connect():
    return psycopg2.connect(DATABASE_URL)

def save_chunks(document_id:str , username:str , content:str , embedding:list[float], chunk_index:int ):

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
            
            INSERT INTO document_chunks 
                        (document_id, username, content, embedding, chunk_index)
            VALUES( %s , %s , %s , %s , %s )
            """

              , (document_id, username, content, embedding, chunk_index))

    conn.commit()
    cursor.close()
    conn.close()

def search_chunks(question_embedding:list[float], username :str , top_k:int = 5) -> list[str]:

        conn = connect()
        cursor = conn.cursor()
        cursor.execute( """
            SELECT content 
            FROM document_chunks
            WHERE username=%s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (username,question_embedding ,top_k)
                )

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return [row[0] for row in results]



def delete_chunks(document_id:str , username:str):
        con = connect()
        cursor = con.cursor()

        cursor.execute("""
                DELETE 
                FROM document_chunks
                WHERE document_id=%s AND username=%s
            """, (document_id, username))

        con.commit()
        cursor.close()
        con.close()