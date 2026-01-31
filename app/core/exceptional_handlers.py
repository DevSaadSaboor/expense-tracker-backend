from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.core.response_builders import error_response

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content=error_response(
            exc.code,
            exc.message,
            exc.details
        ).model_dump()
    )
