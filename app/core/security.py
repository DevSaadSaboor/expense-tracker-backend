import bcrypt
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
import secrets
SECRET_KEY = "super-secret-key-change-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get('sub')

        if user_id is None:
            raise ValueError('Invalid token')
        return int(user_id)
    except JWTError:
        raise ValueError('invalid or expired token')

def create_refresh_token():
    return secrets.token_urlsafe(64)

def refresh_expire_token():
    return datetime.now(timezone.utc) + timedelta(days=14)


def refresh_expires_at():
    return   datetime.now(timezone.utc) + timedelta(days=14)



def hash_password(password: str) -> str:
    # convert string → bytes
    password_bytes = password.encode("utf-8")

    # generate salt + hash
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # store as string in DB
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    # convert both to bytes
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    # check password against hash
    return bcrypt.checkpw(password_bytes, hash_bytes)
