from app.storage.users_repo import create_user,update_user,list_users,delete_user,get_user_by_id,get_user_by_lognin
from app.core.security import hash_password,verify_password
from app.core.exceptions import InvalidUserInput,EmailAlreadyExists,UserNotFound
import sqlite3


def service_create_user(name:str , email:str, password):
    if not name:
          raise InvalidUserInput("Username is required")
    if not email:
          raise InvalidUserInput("Email is required")
    if not password or len(password) <6:
         raise InvalidUserInput('Password length should be greater than 6')
    password_hash = hash_password(password)
    try:
        user = create_user(name=name,email=email,password_hash=password_hash)
    except sqlite3.IntegrityError:
            raise EmailAlreadyExists('Email Already exists')
    return user



def list_user_service(limit, offset):
     if offset < 0:
          raise InvalidUserInput("offset must be >= 0")
     if limit <= 0:
          raise InvalidUserInput("limit must be > 0")
     return list_users(limit,offset)


def delete_user_service(user_id):
     deleted  = delete_user(user_id)

     if not deleted:
          raise UserNotFound('User with this id not found')
     return True


def update_user_service(user_id, fields):    
   
     allowed_field = ['name', 'email']  
     clean_field = {}

     for key,value in fields.items():
          if key in allowed_field:
               clean_field[key]= value

     if not clean_field:
          raise InvalidUserInput("Enter correct field")

     user = update_user(user_id, clean_field)
     if not user:
          raise UserNotFound("user with this id not found")
     return user

def service_get_user_by_id(user_id):
     user_id = get_user_by_id(user_id)
     if user_id is None:
          raise InvalidUserInput('Invalid user id ')
     return user_id


