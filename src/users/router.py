from fastapi import APIRouter, status

from ..dependencies import DatabaseDep
from .schemas import UserCreate, UserPublic
from .services import create_user

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
