from app.storage.users_repo import get_user_by_lognin
from app.core.security import verify_password
from app.core.exceptions import InvalidUserInput

def login_user(email:str,password:str):
     if not email.strip():
          raise InvalidUserInput('Email is required')
     if not password:
          raise InvalidUserInput('password is required')
     
     user = get_user_by_lognin(email)

     if user is None:
          raise InvalidUserInput("email or password is invalid ")
     
     if not verify_password(password,user['password_hash']):
          raise InvalidUserInput('email or password is invalid')
     
     return user['id']
