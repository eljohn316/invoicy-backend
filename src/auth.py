from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from .config import settings
from .dependencies import DatabaseDep
from .exceptions import UnauthorizedException
from .users import models

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def verify_access_token(token: str) -> str | None:
    """Verify a JWT access token and return the subject (user id) if valid."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]},
        )
        return payload.get("sub")
    except jwt.InvalidTokenError:
        return None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DatabaseDep
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise UnauthorizedException(detail="Invalid or expired token")

    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise UnauthorizedException(detail="Invalid or expired token")

    current_user = await db.get(models.User, user_id_int)
    if current_user is None:
        raise UnauthorizedException(detail="User not found")

    return current_user


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]
