from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.auth_service import login_user
from app.service.user_service import service_create_user
from app.service.refresh_service import issue_refresh_token
from app.core.security import create_access_token
from app.core.exceptions import InvalidUserInput
from app.utils.response import ok,fail
from app.utils.error_codes import INVALID_CREDENTIALS
from app.core.security import create_access_token
from app.service.refresh_service import rotate_refresh_token,logout_user
router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class RegisterResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

class RefreshRequest(BaseModel):
    refresh_token : str

class LogoutRequest(BaseModel):
    refresh_token : str

@router.post("/register", status_code=201)
def register(payload: RegisterRequest):
    try:
        user = service_create_user(
            name=payload.name,
            email=payload.email,
            password=payload.password,
        )
        return ok(user)
    except InvalidUserInput as e:
        return fail(INVALID_CREDENTIALS,str(e))

@router.post("/login")

def login(payload: LoginRequest):
    try:
        user_id = login_user(payload.email, payload.password)
        access = create_access_token(user_id)
        refresh = issue_refresh_token(user_id)

    
        return ok({
        "access_token": access,
        "refresh_token": refresh
        })
        
    except InvalidUserInput as e:
        return fail(INVALID_CREDENTIALS,str(e))

@router.post('/refresh')

def refresh(payload:RefreshRequest):
    try:
        new_access = rotate_refresh_token(payload.refresh_token)
        return ok(new_access)
    
    except InvalidUserInput as e:
        return fail('Invalid Refresh Token', str(e))
    
@router.post("/logout")

def logout(payload:LogoutRequest):
        delete = logout_user(payload.refresh_token)
        return ok({"logged_out": True})



