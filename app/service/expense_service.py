from app.core.exceptions import InvalidUserInput,EmailAlreadyExists,UserNotFound
from app.storage.expenses_repo import get_monthly_totals_between_dates,get_monthly_category_totals,get_category_month_total,get_category_totals,get_expenses_with_category,get_expense_by_category,get_expenses_by_user,create_expense,update_expense,get_expenses_by_id,get_expenses_paginated,delete_expense
from app.storage.categories_repo import get_category_by_id
import sqlite3
from datetime import datetime

def is_valid_date(date_str):
    try:    
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def service_create_expense(user_id, category_id, amount, note, spend_at):
    if amount <= 0:
        raise InvalidUserInput('Amount should be grate than zero ')
    if not is_valid_date(spend_at):
        raise InvalidUserInput('Date is Invalid Use YYYY-MM-DD format')
    if category_id is not None:
        category = get_category_by_id(category_id,user_id)
        if category is None:
            raise InvalidUserInput('Category does not belong to this user')
    try:
        new_create_expense= create_expense(user_id, category_id, amount, note, spend_at)
    except sqlite3.IntegrityError:
        raise InvalidUserInput("invalid input")
    return new_create_expense


def service_update_expense(user_id,expense_id,fields:dict):

    expense = get_expenses_by_id(user_id,expense_id)
    if not expense:
        raise InvalidUserInput("Expense not found ")
    allowed= ['amount', 'note', 'spend_at','category_id']
    new_field = {}
    for key,value in fields.items():
        if key in allowed :
            new_field[key] = value
    if not new_field:
        raise InvalidUserInput("No Field need  to be updated ")
    if "amount" in new_field:
        if new_field['amount'] <= 0:
            raise InvalidUserInput('Amount must be greater than zero')
    if "spend_at" in new_field:
        if not  is_valid_date(new_field['spend_at']):
            raise InvalidUserInput("Incoreect date format")
    if "category_id" in new_field:
        cat_id = new_field['category_id']
        if cat_id is not None:
            if get_category_by_id(cat_id,user_id) is None:
                raise InvalidUserInput("category dones not belong to user")
    try:
        update_expenses = update_expense(expense_id = expense_id, user_id = user_id , fields = new_field)
    except sqlite3.IntegrityError:
        raise InvalidUserInput("invalid update data")
    if update_expenses is None:
        raise InvalidUserInput("failed to update")
    return update_expenses


def service_delete_expense(user_id, expense_id):
    expense = get_expenses_by_id(user_id,expense_id)
    if expense is None:
        raise InvalidUserInput("Expense does not found")
    delete = delete_expense(expense_id,user_id)
    if not delete:
        raise InvalidUserInput('Deleted Failed')
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















