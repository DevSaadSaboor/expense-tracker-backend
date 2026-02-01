from datetime import datetime
from app.storage.db import get_connection

def insert_refresh_token(user_id: int, token: str, expires_at):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (%s,%s,%s)
        """,
        (user_id, token, expires_at.isoformat())
    )
    connection.commit()

def get_refresh_token(token: str):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(
        """
        SELECT id, user_id, token, expires_at, revoked
        FROM refresh_tokens
        WHERE token = %s
        """,
        (token,)
    )
    return cur.fetchone()


def revoke_refresh_token(token: str):
     connection = get_connection()
     cur = connection.cursor()
     cur.execute(
        """
        UPDATE refresh_tokens
        SET revoked = 1
        WHERE token = %s
        """,
        (token,)
    )
     connection.commit()

