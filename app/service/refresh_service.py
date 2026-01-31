from datetime import datetime,timezone
from app.storage.refresh_tokens import insert_refresh_token, get_refresh_token,revoke_refresh_token
from app.core.security import create_access_token, create_refresh_token, refresh_expires_at
from app.core.exceptions import InvalidUserInput
from app.storage.db import get_connection   # ← your real DB


def issue_refresh_token(user_id: int):
    conn = get_connection()
    token = create_refresh_token()
    expires = refresh_expires_at()

    insert_refresh_token(conn, user_id, token, expires)
    return token


def rotate_refresh_token(refresh_token: str):
    conn = get_connection()
    row = get_refresh_token(conn, refresh_token)

    if not row:
        raise InvalidUserInput("Invalid refresh token")

    token_id, user_id, token, expires_at, revoked = row

    if revoked:
        raise InvalidUserInput("Refresh token revoked")

    if datetime.fromisoformat(expires_at) < datetime.now(timezone.utc)  :
        raise InvalidUserInput("Refresh token expired")

    return create_access_token(user_id)

def logout_user(refresh_token:str):
    conn = get_connection()
    revoke_refresh_token(conn, refresh_token)































# from datetime import datetime
# from app.storage.refresh_tokens import (
#     insert_refresh_token,
#     get_refresh_token,
#     revoke_refresh_token,
# )
# from app.core.security import create_access_token,create_refresh_token,refresh_expires_at
# from app.core.exceptions import InvalidUserInput
# from app.storage.db import get_connection


# def issue_refresh_token(user_id: int):
   
#     conn = get_connection()
#     token = create_refresh_token()
#     expires = refresh_expires_at()

#     insert_refresh_token(conn, user_id, token, expires)

#     return token


# def rotate_refresh_token(refresh_token: str):
#     conn = get_connection()
#     row = get_refresh_token(conn, refresh_token)

#     if not row:
#         raise InvalidUserInput("Invalid refresh token")

#     token_id, user_id, token, expires_at, revoked = row

#     if revoked:
#         raise InvalidUserInput("Refresh token revoked")

#     if datetime.fromisoformat(expires_at) < datetime.utcnow():
#         raise InvalidUserInput("Refresh token expired")

#     # issue new access token
#     return create_access_token(user_id)
