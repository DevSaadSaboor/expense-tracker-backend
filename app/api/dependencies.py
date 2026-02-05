from fastapi import Depends, HTTPException, status,Security
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.core.observability.context import set_user_id
from app.core.logging import logger
from fastapi import Request

security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> int:
    try:
        token = credentials.credentials
        user_id = decode_access_token(token)
        return int(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

# def get_current_user_id(credentials = Security(security)) -> int:
#     token = getattr(credentials, "credentials", None)
#     try:
#         user_id = decode_access_token(token)
#         if user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#         return int(user_id)
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

# def get_current_user_id(credentials = Security(security)) -> int:
#     try:
#         token = credentials.credentials
#         user_id = decode_access_token(token)

#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired token"
#             )

#         return user_id

#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )


