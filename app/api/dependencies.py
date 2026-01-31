from fastapi import Depends, HTTPException, status,Security
from fastapi.security import HTTPBearer
from app.core.security import decode_access_token


security = HTTPBearer()

def get_current_user_id(credentials = Security(security)) -> int:
    try:
        token = credentials.credentials
        user_id = decode_access_token(token)
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
