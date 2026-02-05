from contextvars import ContextVar

_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)
_user_id: ContextVar[int | None] = ContextVar("user_id", default=None)
_operation: ContextVar [str | None] = ContextVar("operation", default=None)


# --- setters ---
def set_request_id(value: str) -> None:
    return _request_id.set(value)

def set_user_id(value: int | None) -> None:
    return _user_id.set(value)

def set_operation(value: str) -> None:
    return _operation.set(value)


# --- getters ---
def get_request_id() -> str | None:
    return _request_id.get()

def get_user_id() -> int | None:
    return _user_id.get()

def get_operation() -> str | None:
    return _operation.get()

# --- Resetters ----
def reset_request_id(token):
    _request_id.reset(token)

def reset_user_id(token):
    _user_id.reset(token)

def reset_operation(token):
    _operation.reset(token)
