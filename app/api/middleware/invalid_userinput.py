from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging import logger
from app.core.exceptions import InvalidUserInput

async def invalid_user_input_handler(request: Request, exc: InvalidUserInput):
    logger.warning(
        "request_failed",
        error_type="InvalidUserInput",
        message=str(exc),
        path=request.url.path,
    )

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": str(exc),
            "data": None,
        },
    )
