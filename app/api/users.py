from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_current_user_id
from pydantic import BaseModel
from typing import Optional
from app.service.user_service import (
    service_get_user_by_id,
    update_user_service,
)
from app.core.exceptions import InvalidUserInput, UserNotFound
from app.utils.response import ok,fail
from app.utils.error_codes import CATEGORY_NOT_FOUND,EXPENSE_NOT_FOUND,INVALID_AMOUNT,INVALID_CREDENTIALS

class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    created_at : str

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email : Optional[str]  = None




router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_my_profile(user_id: int = Depends(get_current_user_id)):
    try:
        my_profile =  service_get_user_by_id(user_id)
        return ok(my_profile)
    except UserNotFound as e:
        return fail(INVALID_CREDENTIALS,str(e))
    


@router.patch("/me")
def update_my_profile(
    payload: UserUpdateRequest,
    user_id: int = Depends(get_current_user_id),
):
    try:
        fields = payload.model_dump(exclude_unset=True)
        return ok(update_user_service(user_id, fields))
    except InvalidUserInput as e:
        return fail(INVALID_CREDENTIALS, str(e))
    except UserNotFound as e:
         return fail(INVALID_CREDENTIALS, str(e))
