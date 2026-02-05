from app.storage.users_repo import get_user_by_lognin
from app.core.security import verify_password
from app.core.exceptions import InvalidUserInput
from app.storage.users_repo import create_user
from app.core.logging import logger
from app.storage.refresh_tokens import revoke_refresh_token


def register_user(name: str, email: str, password: str):
    logger.info(
        "user_register_started",
        email=email,
    )

    if not name.strip():
        logger.warning(
            "user_register_failed",
            reason="name_missing",
            email=email,
        )
        raise InvalidUserInput("Name is required")

    if not email.strip():
        logger.warning(
            "user_register_failed",
            reason="email_missing",
            email=email,
        )
        raise InvalidUserInput("Email is required")

    if not password:
        logger.warning(
            "user_register_failed",
            reason="password_missing",
            email=email,
        )
        raise InvalidUserInput("Password is required")

    try:
        user_id = create_user(name, email, password)
    except Exception:
        logger.warning(
            "user_register_failed",
            reason="email_already_exists",
            email=email,
        )
        raise InvalidUserInput("User already exists")

    logger.info(
        "user_registered",
        user_id=user_id,
    )

    return user_id

def login_user(email: str, password: str):
    logger.info(
        "login_attempt",
        email=email,
    )

    if not email.strip():
        logger.warning(
            "login_failed",
            reason="email_missing",
            email=email,
        )
        raise InvalidUserInput("Email is required")

    if not password:
        logger.warning(
            "login_failed",
            reason="password_missing",
            email=email,
        )
        raise InvalidUserInput("Password is required")

    user = get_user_by_lognin(email)
    if user is None:
        logger.warning(
            "login_failed",
            reason="user_not_found",
            email=email,
        )
        raise InvalidUserInput("Email or password is invalid")

    if not verify_password(password, user["password_hash"]):
        logger.warning(
            "login_failed",
            reason="invalid_password",
            user_id=user["id"],
        )
        raise InvalidUserInput("Email or password is invalid")

    logger.info(
        "login_success",
        user_id=user["id"],
    )

    return user["id"]

def logout_user(user_id: int, refresh_token: str):
    logger.info(
        "logout_started",
        user_id=user_id,
    )

    deleted = revoke_refresh_token(refresh_token)

    if not deleted:
        logger.warning(
            "logout_failed",
            reason="token_not_found",
            user_id=user_id,
        )

    logger.info(
        "logout_success",
        user_id=user_id,
    )

    return True