from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import (
    CurrentUserDep,
    create_access_token,
    verify_password,
)
from ..dependencies import DatabaseDep
from ..exceptions import UnauthorizedException
from .schemas import Token, UserCreate, UserPrivate, UserPublic
from .services import create_user, get_user_by_email

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
        raise UnauthorizedException(detail="Invalid email or password")

    if not verify_password(form_data.password, user.password_hash):
        raise UnauthorizedException(detail="Invalid email or password")

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token, token_type="Bearer")


@router.get(
    "/current-user",
    name="Get currently authenticated user",
    response_model=UserPrivate,
)
async def get_current_user_handler(current_user: CurrentUserDep):
    return current_user
