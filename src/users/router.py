from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import CurrentUserDep, create_access_token, verify_password
from ..dependencies import DatabaseDep
from ..exceptions import BadRequestException, UnauthorizedException
from .schemas import (
    Message,
    Token,
    UserCreate,
    UserPrivate,
    UserPublic,
    UserUpdate,
    UserUpdatePassword,
)
from .services import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: DatabaseDep):
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "/",
    name="Create user",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_handler(user_data: UserCreate, user_service: UserServiceDep):
    new_user = await user_service.create_user(user_data)
    return new_user


@router.post("/token", name="Authenticate user", response_model=Token)
async def login_user_handler(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
):
    user = await user_service.get_user_by_email(form_data.username)
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


@router.patch(
    "/current-user",
    name="Update currently authenticated user",
    response_model=UserPrivate,
)
async def update_current_user_handler(
    user_data: UserUpdate,
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
):
    updated_user = await user_service.update_current_user(current_user, user_data)
    return updated_user


@router.patch(
    "/current-user/password",
    name="Update currently authenticated user password",
    response_model=Message,
)
async def update_current_user_password_handler(
    user_password_data: UserUpdatePassword,
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
):
    verified = verify_password(user_password_data.password, current_user.password_hash)
    if not verified:
        raise BadRequestException(detail="Incorrect password")

    if user_password_data.password == user_password_data.new_password:
        raise BadRequestException(
            detail="New password cannot be the same as the current one"
        )

    await user_service.update_current_user_password(current_user, user_password_data)
    return Message(message="Password updated successfully")
