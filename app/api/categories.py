from fastapi import APIRouter,status,HTTPException
from pydantic import BaseModel
from app.core.exceptions import InvalidUserInput
from app.service.categories_service import service_delete_category,service_update_category,service_create_category,service_get_category_by_id,service_get_categories_by_user
router = APIRouter(prefix="/categories", tags=["categories"])
from typing import List,Optional
from fastapi import Depends
from app.api.dependencies import get_current_user_id
from app.utils.response import ok,fail
from app.utils.error_codes import CATEGORY_NOT_FOUND
from app.core.logging import logger

class CategoriesCreateRequest(BaseModel):
    name: str

class CategoriesResponse(BaseModel):
    id: int
    user_id: int
    name:str

class CategoriesUpdateRequest(BaseModel):
    name : Optional[str] = None
@router.post("/",status_code= status.HTTP_201_CREATED)

def create_category_endpoint(payload: CategoriesCreateRequest, user_id: int = Depends(get_current_user_id)):    
    try:
        category = service_create_category(
        user_id=user_id,
        name = payload.name
    )
    except InvalidUserInput as e:
        return fail(CATEGORY_NOT_FOUND,str(e))
    return ok(category)

@router.get("/{category_id}")

def get_category_by_id_endpoint(category_id:int,user_id: int = Depends(get_current_user_id)):
    
    try:
        category = service_get_category_by_id(user_id,category_id)
    except InvalidUserInput as e :
        return fail(CATEGORY_NOT_FOUND,str(e))
    return ok(category)

@router.get("/")

def get_categories_byuser_endpoint(user_id: int = Depends(get_current_user_id)):
    category = service_get_categories_by_user(user_id)
    return ok(category)

@router.patch("/{category_id}" )

def get_update_endpoint(category_id:int,payload:CategoriesUpdateRequest,user_id: int = Depends(get_current_user_id)):
    try:
        update = service_update_category(
        user_id=user_id,
        category_id= category_id,
        fields=payload.model_dump(exclude_unset=True)
    )
    except InvalidUserInput as e:
        return fail(CATEGORY_NOT_FOUND,str(e))
    return ok(update)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)

def get_delete_endpoint(category_id:int,user_id: int = Depends(get_current_user_id)):   
    try:
        delete = service_delete_category(user_id,category_id)
    except InvalidUserInput as e :
        return fail(CATEGORY_NOT_FOUND,str(e))
    return ok(None)