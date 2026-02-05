import uuid
import time
from fastapi import Request
from app.core.logging import logger

from app.core.observability.context import (
    set_request_id,
    set_user_id,
    set_operation,
    reset_operation,
    reset_request_id,
    reset_user_id
)


async def request_context_middleware(request: Request, call_next):
    stat_time = time.perf_counter()
    response = None

    request_id = uuid.uuid4().hex
    operation = f"{request.method} {request.url.path}"

    req_token = set_request_id(request_id)
    op_token = set_operation(operation)
    # user_token = set_user_id(None)

    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.perf_counter() - stat_time) * 1000)
        logger.info(
            "request_completed",
            method = request.method,
            path = request.url.path,
            status_code = getattr(response, 'status_code', None),
            duration_ms = duration_ms
        )   
        reset_request_id(req_token)
        reset_operation(op_token)
        # reset_user_id(user_token)