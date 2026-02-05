from app.core.exceptions import InvalidUserInput
from app.storage.categories_repo import get_categories_by_user,create_category,get_category_by_id,update_category,delete_category
import sqlite3
from app.core.logging import logger


def service_create_category(user_id:int, name:str):
        logger.info("category_create_started",user_id=user_id,name=name)
        name = name.strip()
        if name == "":
          logger.warning (
            "category_create_failed",
            reason="empty_name",
            user_id=user_id,
          )
          raise InvalidUserInput("Name should not be empty")
        try:
          category = create_category(user_id,name)
        except sqlite3.IntegrityError:
          logger.warning(
            "category_create_failed",
            reason="duplicate_category",
            user_id=user_id,
            name=name,)  
          raise InvalidUserInput("Category already exists")
        logger.info(
           "category_created",
          user_id=user_id,
          category_id=category["id"],
          name=category["name"],
        )
        return category
  
def service_update_category(user_id, category_id,fields:dict):
    logger.info(
         "category_update_started",
        user_id=user_id,
        category_id=category_id,
    )
    
    cat_id = get_category_by_id(category_id,user_id)
    if not cat_id:
      logger.warning(
          "category_update_failed",
            reason="category_not_found",
            user_id=user_id,
            category_id=category_id,
        )
      raise InvalidUserInput("category not found")
    allowed = ['name']
    clean_field = {}
    for key,value in fields.items():
      if key in allowed:
        clean_field[key] = value
    if not clean_field:
      logger.warning(
           "category_update_failed",
            reason="no_fields_to_update",
            user_id=user_id,
            category_id=category_id,
      )
      raise InvalidUserInput('not field need to update')
    
    if 'name' in clean_field:
      if clean_field['name'].strip() == "":
        logger.warning(
            "category_update_failed",
            reason="empty_name",
            user_id=user_id,
            category_id=category_id,
        )
        raise InvalidUserInput('Name should not be empty')
    try:
        category = update_category(category_id,user_id,clean_field)
    except sqlite3.IntegrityError:
        logger.warning(
            "category_update_failed",
            reason="duplicate_category",
            user_id=user_id,
            category_id=category_id,
        )
        raise InvalidUserInput('Fail to update')
    if not category:
        logger.warning(
            "category_update_failed",
            reason="nothing_updated",
            user_id=user_id,
            category_id=category_id,
        )
        raise InvalidUserInput('Nothing to update')
    
    logger.info(
        "category_updated",
        user_id=user_id,
        category_id=category_id,
    ) 
    return category

def service_delete_category(user_id,category_id):
    logger.info("category_delete_started",user_id=user_id,category_id = category_id)
    cat_id = get_category_by_id(category_id,user_id)
    if not cat_id:
       logger.warning(
          "category_delete_failed",
            reason="category_not_found",
            user_id=user_id,
            category_id=category_id,
       )
       raise InvalidUserInput('category not found')
    delete = delete_category(category_id,user_id)
    if not delete:
        logger.warning(
            "category_delete_failed",
            reason="delete_failed",
            user_id=user_id,
            category_id=category_id,
        )
        raise InvalidUserInput('No category found to delete')
    logger.info(
        "category_deleted",
        user_id=user_id,
        category_id=category_id,
    )
    return True

def service_get_categories_by_user(user_id):
   category = get_categories_by_user(user_id)
   return category

def service_get_category_by_id(user_id,category_id):
    cat_id = get_category_by_id(category_id,user_id)
    if cat_id is None:
       raise InvalidUserInput('Category not found')
    return cat_id



