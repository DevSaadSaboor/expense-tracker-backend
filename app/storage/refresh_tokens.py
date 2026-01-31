from datetime import datetime

def insert_refresh_token(conn, user_id: int, token: str, expires_at):
    conn.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (?, ?, ?)
        """,
        (user_id, token, expires_at.isoformat())
    )
    conn.commit()

def get_refresh_token(conn, token: str):
    cur = conn.execute(
        """
        SELECT id, user_id, token, expires_at, revoked
        FROM refresh_tokens
        WHERE token = ?
        """,
        (token,)
    )
    return cur.fetchone()


def revoke_refresh_token(conn, token: str):
    conn.execute(
        """
        UPDATE refresh_tokens
        SET revoked = 1
        WHERE token = ?
        """,
        (token,)
    )
    conn.commit()

