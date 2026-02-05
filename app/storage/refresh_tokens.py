from datetime import datetime
from app.storage.db import get_connection
from psycopg2.extras import RealDictCursor


def insert_refresh_token(user_id: int, token: str, expires_at):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (%s,%s,%s)
        """,
        (user_id, token, expires_at)
    )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()
        connection.close()

def get_refresh_token(token: str):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
        """
        SELECT id, user_id, token, expires_at, revoked
        FROM refresh_tokens
        WHERE token = %s
        """,
        (token,)
    )
        return cur.fetchone()
    finally:
        cur.close()
        connection.close()

def revoke_refresh_token(token: str):
     connection = get_connection()
     cur = connection.cursor(cursor_factory=RealDictCursor)
     try:
        cur.execute(
        """
        UPDATE refresh_tokens
        SET revoked = TRUE
        WHERE token = %s
        """,
        (token,)
    )
        connection.commit()
     except Exception:
         connection.rollback()
         raise
     finally:
         cur.close()
         connection.close()

