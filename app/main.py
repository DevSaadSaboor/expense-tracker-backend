from fastapi import FastAPI
from  pathlib import Path
from app.api.users import router as user_router 
from app.api.categories import router as category_router
from app.api.expenses import router as expense_router
from app.api.auth import router as login_router
# from app.core.exceptional_handlers import app_exception_handler
# from app.core.exceptions import AppException

app = FastAPI()
# app.add_exception_handler(AppException, app_exception_handler)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(expense_router)




# from app.storage.db import create_table

# if __name__ == "__main__":
#     create_table()
#     print("✅ Database initialized successfully")