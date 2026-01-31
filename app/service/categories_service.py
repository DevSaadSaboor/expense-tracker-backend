from app.core.exceptions import InvalidUserInput,EmailAlreadyExists,UserNotFound
from app.storage.categories_repo import get_categories_by_user,create_category,get_category_by_id,update_category,delete_category
import sqlite3

def service_create_category(user_id:int, name:str):
  name = name.strip()
  if name == "":
        raise InvalidUserInput("Name should not be empty")
  try:
    return create_category(user_id,name)
  except sqlite3.IntegrityError:
    raise InvalidUserInput("Category already exists")
  
def service_update_category(user_id, category_id,fields:dict):
    cat_id = get_category_by_id(category_id,user_id)
    if not cat_id:
      raise InvalidUserInput("category not found")
    allowed = ['name']
    clean_field = {}
    for key,value in fields.items():
      if key in allowed:
        clean_field[key] = value
    if not clean_field:
      raise InvalidUserInput('not field need to update')
    
    if 'name' in clean_field:
      if clean_field['name'].strip() == "":
        raise InvalidUserInput('Name should not be empty')
    try:
        category = update_category(category_id,user_id,clean_field)
    except sqlite3.IntegrityError:
        raise InvalidUserInput('Fail to update')
    if category is None:
      raise InvalidUserInput('Nothing to update')
    return category

def service_delete_category(user_id,category_id):
    cat_id = get_category_by_id(category_id,user_id)
    if not cat_id:
       raise InvalidUserInput('category not found')
    delete = delete_category(category_id,user_id)
    if not delete:
       raise InvalidUserInput('No category found to delete')
    return True

def service_get_categories_by_user(user_id):
   category = get_categories_by_user(user_id)
   return category

def service_get_category_by_id(user_id,category_id):
    cat_id = get_category_by_id(category_id,user_id)
    if cat_id is None:
       raise InvalidUserInput('Category not found')
    return cat_id



