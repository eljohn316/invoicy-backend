from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..auth import hash_password
from .schemas import UserCreate


class UserService:
    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    async def create_user(self, user_data: UserCreate):
        user_exists = await self.get_user_by_email(user_data.email)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        new_user = models.User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)

        return new_user

    async def get_user_by_email(self, email: str):
        result = await self._db.execute(
            select(models.User).where(models.User.email == email)
        )
        user = result.scalars().first()
        return user
