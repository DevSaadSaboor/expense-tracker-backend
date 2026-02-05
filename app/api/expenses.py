from fastapi import APIRouter,status,HTTPException,Depends
from pydantic import BaseModel
from app.core.exceptions import InvalidUserInput
from app.api.dependencies import get_current_user_id
router = APIRouter(prefix="/expenses", tags=["expenses"])
from typing import List,Optional
from app.utils.response import ok,fail
from app.service.expense_service import service_delete_expense,service_create_expense,service_get_expense_by_id,service_get_expenses_page,service_update_expense
from app.utils.error_codes import EXPENSE_NOT_FOUND
from app.core.logging import logger

class ExpenseCreateRequest(BaseModel):
    category_id :Optional[int] = None
    amount: int
    note: str
    spend_at : str

class ExpenseResponse(BaseModel):
    id:int
    user_id :int
    category_id :Optional[int]
    amount:int
    note:str
    spend_at:str
    created_at:str

class ExpenseUpdateRequest(BaseModel):
    amount : Optional[int] = None
    note : Optional[str] = None
    spend_at: Optional[str] = None
    category_id : Optional[int] = None 

# @router.post("",response_model = ExpenseResponse , status_code = status.HTTP_201_CREATED)
router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_current_user_id)]  
)
@router.post("/", status_code = status.HTTP_201_CREATED)

def create_expense_endpoint(payload:ExpenseCreateRequest, user_id: int = Depends(get_current_user_id)):
    # logger.info("expense_created", user_id =user_id, amount = payload.amount,category_id = payload.category_id)
    expense = service_create_expense(
        user_id=user_id,
        category_id=payload.category_id,
        amount=payload.amount,
        note = payload.note,
        spend_at=payload.spend_at,
    )
    return ok(expense)
    

    # try:
    #     expense = service_create_expense(
    #         user_id = user_id,
    #         category_id = payload.category_id,
    #         amount = payload.amount,
    #         note = payload.note,
    #         spend_at = payload.spend_at
    #     )
    # except InvalidUserInput as i:
    #     return fail(EXPENSE_NOT_FOUND,str(i))
    # return ok(expense)
    
# @router.get("/{expense_id}", response_model=ExpenseResponse, status_code= status.HTTP_200_OK)
@router.get("/{expense_id}", status_code= status.HTTP_200_OK)
def get_expense_endpoint(expense_id:int, user_id :int = Depends(get_current_user_id) ):
   
    try:
        expense = service_get_expense_by_id(expense_id,user_id)
    except InvalidUserInput as i :
        return fail(EXPENSE_NOT_FOUND,str(i))
    return ok(expense)

@router.get("/")
# @router.get("",response_model= List[ExpenseResponse])

def get_expenses_endpoint(limit:int,offset:int, user_id :int = Depends(get_current_user_id)):
   
    try:
        expenses = service_get_expenses_page(user_id,limit,offset,)
    except InvalidUserInput as e:
         return fail(EXPENSE_NOT_FOUND,str(e))
    return ok(expenses)

# @router.patch("/{expense_id}", response_model= ExpenseResponse)
@router.patch("/{expense_id}")

def update_expense_endpoint(expense_id:int,payload:ExpenseUpdateRequest,user_id :int = Depends(get_current_user_id)):
    # logger.info("expense_updated", user_id_param=user_id, expense_id = expense_id)
    try:
        update = service_update_expense(
        user_id= user_id,
        expense_id=expense_id,
        fields=payload.model_dump(exclude_unset = True)
    )  
    except InvalidUserInput as e:
         return fail(EXPENSE_NOT_FOUND,str(e))
    return ok(update)

# @router.delete("/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{expense_id}",status_code=status.HTTP_200_OK)

def delete_expense_endpoint(expense_id:int,user_id :int = Depends(get_current_user_id)):
    # logger.info("create_expense", user_id_param=user_id, expense_id= expense_id)
    try:
        delete = service_delete_expense(user_id,expense_id)
    except InvalidUserInput as e:
         return fail(EXPENSE_NOT_FOUND,str(e))
    return ok(None)
