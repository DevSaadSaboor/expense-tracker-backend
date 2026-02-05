from fastapi import FastAPI
from app.api.users import router as user_router 
from app.api.categories import router as category_router
from app.api.expenses import router as expense_router
from app.api.auth import router as login_router
from app.api.middleware.requestcontext import request_context_middleware
from app.api.middleware.exceptional_handler import unhandled_exception_handler
from app.api.middleware.invalid_userinput import invalid_user_input_handler
from app.core.exceptions import InvalidUserInput

app = FastAPI()

app.middleware("http")(request_context_middleware)
app.add_exception_handler(InvalidUserInput,invalid_user_input_handler)
app.add_exception_handler(Exception,unhandled_exception_handler)

app.include_router(login_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(expense_router)




# from app.storage.db import create_table

# if __name__ == "__main__":
#     create_table()
#     print("✅ Database initialized successfully")