from fastapi import HTTPException, status,Security
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.core.security import decode_access_token

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
