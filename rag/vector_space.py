import psycopg2
from config import DATABASE_URL


def connect():
    return psycopg2.connect(DATABASE_URL)


def save_chunks(document_id: str, username: str, content: str,
                embedding: list[float], chunk_index: int):
    if not all([document_id, username, content, embedding]):
        raise ValueError("All fields required")

    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO document_chunks
                (document_id, username, content, embedding, chunk_index)
            VALUES (%s, %s, %s, %s, %s)
        """, (document_id, username, content, embedding, chunk_index))
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Error saving chunks: {e}")
    finally:
        conn.close()


def search_chunks(question_embedding: list[float],
                  username: str, top_k: int = 5) -> list[str]:
    if not question_embedding:
        raise ValueError("Embedding cannot be empty")
    if not username or not username.strip():
        raise ValueError("Username is required")

    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT content
            FROM document_chunks
            WHERE username = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (username, question_embedding, top_k))
        results = cursor.fetchall()
        cursor.close()
        return [row[0] for row in results]
    except Exception as e:
        raise RuntimeError(f"Search failed: {e}")
    finally:
        conn.close()


def delete_chunks(document_id: str, username: str):
    if not document_id or not username:
        raise ValueError("document_id and username required")

    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM document_chunks
            WHERE document_id = %s AND username = %s
        """, (document_id, username))
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Delete failed: {e}")
    finally:
        conn.close()