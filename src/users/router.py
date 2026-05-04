from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import (
    create_access_token,
    oauth2_scheme,
    verify_access_token,
    verify_password,
)
from ..dependencies import DatabaseDep
from .schemas import Token, UserCreate, UserPrivate, UserPublic
from .services import create_user, get_user_by_email, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    name="Create user",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_handler(user: UserCreate, db: DatabaseDep):
    new_user = await create_user(db, user)
    return new_user


@router.post("/token", name="Authenticate user", response_model=Token)
async def login_user_handler(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DatabaseDep,
):
    user = await get_user_by_email(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token, token_type="Bearer")


@router.get(
    "/current-user",
    name="Get currently authenticated user",
    response_model=UserPrivate,
)
async def get_current_user_handler(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DatabaseDep,
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = await get_user_by_id(db, user_id_int)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
