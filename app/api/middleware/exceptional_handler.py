from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging import logger

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "unhandled_exception",
        error_type=type(exc).__name__,
        message=str(exc),
        path=request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "data": None,
        },
    )
