from typing import Any
from core.responses import APIResponse, APIError

def success_response(data: Any) -> APIResponse:
    return APIResponse(
        success=True,
        data=data,
        error=None
    )


def error_response(code: str, message: str, details: dict | None = None) -> APIResponse:
    return APIResponse(
        success=False,
        data=None,
        error=APIError(
            code=code,
            message=message,
            details=details
        )
    )
