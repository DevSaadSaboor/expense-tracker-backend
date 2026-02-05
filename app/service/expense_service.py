from app.core.exceptions import InvalidUserInput
from app.storage.expenses_repo import get_monthly_totals_between_dates,get_monthly_category_totals,get_category_month_total,get_category_totals,get_expenses_with_category,get_expense_by_category,get_expenses_by_user,create_expense,update_expense,get_expenses_by_id,get_expenses_paginated,delete_expense
from app.storage.categories_repo import get_category_by_id
import sqlite3
from datetime import datetime
from app.core.logging import logger

def is_valid_date(date_str):
    try:    
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def service_create_expense(user_id, category_id, amount, note, spend_at):
    logger.info("expense_create_started", user_id =user_id, amount = amount,category_id = category_id)
    if amount <= 0:
        logger.warning('expense_create_failed', reason = 'Invalid_amount', amount=amount, user_id = user_id)
        raise InvalidUserInput('Amount should be greater than zero ')
    if not is_valid_date(spend_at):
        logger.warning('expense_create_failed', reason = 'date_invalid', spend_at= spend_at, user_id = user_id)
        raise InvalidUserInput('Date is Invalid Use YYYY-MM-DD format')
    if category_id is not None:
        category = get_category_by_id(category_id,user_id)
        if category is None:
            logger.warning(
                "expense_create_failed",
                reason="category_not_owned",
                category_id=category_id,
                user_id=user_id
            )
            raise InvalidUserInput('Category does not belong to this user')
        
    new_create_expense= create_expense(user_id = user_id, category_id= category_id, amount= amount, note = note, spend_at= spend_at)
    logger.info(
        "expense_created",
        user_id = user_id,
        expense_id=new_create_expense['id'],
        amount=new_create_expense['amount'],
        category_id=new_create_expense['category_id'],
    )
    return new_create_expense


def service_update_expense(user_id,expense_id,fields:dict):
    logger.info("expense_update_started", user_id =user_id, expense_id = expense_id)
    expense = get_expenses_by_id(user_id,expense_id)
    if not expense:
        logger.warning(
            "expense_update_failed", 
            reason = "expense not found", 
            user_id= user_id,
            expense_id=expense_id)
        raise InvalidUserInput("Expense not found ")
    allowed= ['amount', 'note', 'spend_at','category_id']
    new_field = {}
    for key,value in fields.items():
        if key in allowed :
            new_field[key] = value
    if not new_field:
        logger.warning(
            "expense_update_failed", 
            reason = "expense not found", 
            user_id= user_id,
            expense_id=expense_id)
        raise InvalidUserInput("No Field need  to be updated ")
    
    if "amount" in new_field and new_field['amount'] <= 0:
            logger.warning(
            "expense_update_failed",
            reason="invalid_amount",
            user_id=user_id,
        )
            raise InvalidUserInput('Amount must be greater than zero')
    if "spend_at" in new_field and not is_valid_date(new_field['spend_at']):
            logger.warning(
            "expense_update_failed",
            reason="invalid_date",
            user_id=user_id,
        )
        
            raise InvalidUserInput("Incorrect date format")
    if "category_id" in new_field:
        cat_id = new_field['category_id']
        if cat_id is not None and get_category_by_id(cat_id,user_id) is None:
                logger.warning(
                "expense_update_failed",
                reason="invalid_category",
                user_id=user_id,
                category_id=cat_id,
                )
                raise InvalidUserInput("category dones not belong to user")
    update_expenses = update_expense(expense_id = expense_id, user_id = user_id , fields = new_field)
    logger.info(
        'expense_updated',
        user_id = user_id,
        expense_id = expense_id
    )
    return update_expenses
  


def service_delete_expense(user_id, expense_id):
    logger.info("expense_delete_started", user_id =user_id, expense_id = expense_id)
    expense = get_expenses_by_id(user_id,expense_id)
    if not expense :
        logger.warning("expense_delete_failed", reason = "invalid expense", user_id = user_id, expense_id = expense_id)
        raise InvalidUserInput("Expense does not found")
    delete_expense(expense_id,user_id)
    logger.info(
        'expense_deleted',
        user_id = user_id,
        expense_id = expense_id
    )
    return True 


def service_get_expense_by_id(user_id, expense_id):
    get_expense = get_expenses_by_id(user_id,expense_id)
    if get_expense is None:
        raise InvalidUserInput("Expense not found")
    return get_expense


def service_get_expenses_page(user_id, limit, offset):
    if limit <= 0 or limit >100:
        raise InvalidUserInput("Range Limit exceeded")
    if offset < 0:
        raise InvalidUserInput('Offset range exceeded')
    expense_page = get_expenses_paginated(user_id, limit, offset)
    return expense_page

def service_get_expense_by_user(user_id):
    get_expense_user = get_expenses_by_user(user_id)
    return get_expense_user

def service_get_expense_by_category(user_id,category_id):
    if category_id is not None:
        category = get_category_by_id(category_id,user_id)
        if category is None:
            raise InvalidUserInput('Category does not belong to this user')
    service_expense_by_category = get_expense_by_category(user_id,category_id)
    return service_expense_by_category

def service_get_expenses_with_category(user_id):
    get_expenses = get_expenses_with_category(user_id)
    return get_expenses

def service_get_category_totals(user_id):
    category_total = get_category_totals(user_id)
    return category_total

def service_get_category_month_total(user_id):
    category_month_total = get_category_month_total(user_id)
    return category_month_total

def service_get_monthly_category_totals(user_id):
    monthly_category_totals = get_monthly_category_totals(user_id)
    return monthly_category_totals

def service_get_monthly_totals_between_dates(user_id,start_date,end_date):
    if not is_valid_date(start_date):
        raise InvalidUserInput("Invalid date format")
    if not is_valid_date(end_date):
        raise InvalidUserInput("Invalid date format")
    monthly_total_with_dates = get_monthly_totals_between_dates(user_id,start_date,end_date)
    return monthly_total_with_dates















